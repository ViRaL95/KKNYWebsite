from API.newsConnection import NewsConnection
from EMAIL import emailKKNYInfo
from DATABASE.retrieve_event_for_photo_gallery import PreviousEvents 
from DATABASE.renderMembers import CommitteeMembers
from DATABASE.renderEvents import Events
from AWS_S3_PHOTOS.send_image_to_bucket import Photo_Send_s3
import json
import os
import uuid
import hashlib
from flask import Flask, url_for, render_template, request, redirect, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////database/users.db'
application.config['SECRET_KEY'] = 'kkny_secrets'
application.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024
db = SQLAlchemy(application)
login_manager = LoginManager()
login_manager.init_app(application)

class User (UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True)
    password= db.Column(db.String(35))
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    gender = db.Column(db.String(6))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

"""
HTML Files are in the templates directory
homepage.html is rendered with news articles. The news articles are recieved from the newsConnection module in the API Package.
"""
@application.route("/")
def start():
    session.pop('url', None)
    newsConnection = NewsConnection()
    return render_template('homepage.html', news_articles=newsConnection.retrieveNews())
"""
about.html is rendered. 
"""
@application.route("/about")
def renderAboutUs():
    committeeMembers = CommitteeMembers()
    previous_committee = committeeMembers.retrievePreviousCommittee()
    return render_template('about.html', previous_committee=previous_committee);

"""
This method retrieves all members in our MongoDB Database. The module renderMembers in the DATABASE package retrieves all members in our different committees. These different committees are different collections in our MongoDB database.
"""

@application.route("/members")
def renderAllMembers():
    committeeMembers = CommitteeMembers()
    executive_committee = committeeMembers.retrieveExecutiveCommittee()
    contacts = committeeMembers.retrieveContactsList()
    cultural_committee = committeeMembers.retrieveCulturalCommittee()
    youth_committee = committeeMembers.retrieveYouthCommittee()
    food_committee = committeeMembers.retrieveFoodCommittee()
    fundraising_committee = committeeMembers.retrieveFundraisingCommittee()
    sound_music_committee = committeeMembers.retrieveSoundMusicCommittee()
    decorations_committee = committeeMembers.retrieveDecorationsCommittee()
    sports_committee = committeeMembers.retrieveSportsCommittee()
    return render_template("members.html", contacts=contacts, executive_committee=executive_committee, cultural_committee=cultural_committee, youth_committee=youth_committee, food_committee=food_committee, 
                           fundraising_committee=fundraising_committee, sound_music_committee=sound_music_committee, decorations_committee=decorations_committee, sports_committee=sports_committee)


@application.route("/presidentsMessage")
def renderPresidentsMessage():
    session.pop('url', None)
    return render_template('presidents_message.html')


@application.route("/sendSuggestionToSuggestionsBox", methods=['POST'])
def sendEmail():
    suggestion = request.get_json()
    emailKKNYInfo.email_kkny_account(suggestion)
    session.pop('url', None)
    return "success"

@application.route("/contact_us", methods=['GET'])
def contact_us():
    session.pop('url', None)
    return render_template('contact_us_page.html')

@application.route("/upload_pics_page")
def upload_pic_page():
    if current_user.is_authenticated: 
        previous_events = PreviousEvents()
        events = previous_events.retrieve_all_event_info()
        session.pop('url', None)
        return render_template("upload_pictures.html", events=events)
    else:
        session['url'] = '/upload_pics_page'
        print("session set")
        return redirect(url_for("login_page"))


@application.route("/upload_pics/<string:event_name>", methods=['POST'])
@login_required
def upload_pics(event_name):
    previous_events = PreviousEvents()
    event_info = previous_events.retrieve_event_info(event_name=event_name)
    upload_to_s3 = Photo_Send_s3()
    list_of_files = request.files.getlist("file[]")
    return json.dumps(upload_to_s3.send_photo_to_s3(list_of_files, {'email': current_user.email}, event_info))

@application.errorhandler(413)
def request_entity_too_large(error):
    return json.dumps({"message": "Please try to restrict the total size of all images to be less than 25 MB"}), 413, {'ContentType': 'application/json'}

@application.route("/login_page")
def login_page():
    return render_template("login.html")

@application.route("/login", methods=['POST'])
def login():
    user_info = request.get_json()
    email = user_info["email"]
    password = user_info["password"]
    user = User.query.filter_by(email=email).first()
    if not user:
        return json.dumps({"user_exists": False})
    hashed_password, salt = user.password.split(":")
    if hashed_password == hashlib.sha256(salt.encode() + password.encode()).hexdigest():
        if 'url' in session:
            login_user(user)
            return json.dumps({"user_exists": True, "redirect_to": session['url']})
        login_user(user)
        return json.dumps({"user_exists": True})
        

@application.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("start"))
 
@application.route("/sign_up_page")
def signup_page():
    return render_template("sign_up.html")

@application.route("/sign_up", methods=['POST'])
def signup():
    sign_up_info = request.get_json()
    for key, value in sign_up_info.items():
        if value.strip() == "":
            return json.dumps({"user_signed_up": False, "message": "There are missing fields"})
    if sign_up_info['password'] != sign_up_info['repeat_password']:
        return json.dumps({"user_signed_up": False, "message": "Passwords not matching"})
    if len(sign_up_info['password']) > 35:
        return json.dumps({"user_signed_up": False, "message": "Password must not be above 35 characters"})
    if '@' not in sign_up_info["email"] or '.com' not in sign_up_info["email"]:
        return json.dumps({"user_signed_up": False, "message": "Please enter only valid emails"})
    check_if_user_already_exists = User.query.filter_by(email=sign_up_info['email']).first()
    if check_if_user_already_exists:
        return json.dumps({"user_signed_up": False, "message": "A user already exists with this email address"})
    first_name = sign_up_info["first_name"]
    last_name = sign_up_info["last_name"]
    gender = sign_up_info["gender"]
    email = sign_up_info["email"]
    password = sign_up_info["password"]
    repeat_password = sign_up_info["repeat_password"]
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ":" + salt
    user = User(email=email, password=hashed_password, first_name=first_name, last_name=last_name, gender=gender)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return json.dumps({"user_signed_up": True})
   
@application.route("/photo_gallery")
def render_all_photo_events():
    if current_user.is_authenticated:
        previous_events = PreviousEvents()
        all_previous_events = previous_events.retrieve_all_event_info()
        session.pop('url', None)
        return render_template('photo_gallery_events.html', previous_events=all_previous_events)
    else:
        session['url'] = '/photo_gallery'
        return redirect(url_for("login_page"))

if __name__ == "__main__":
    application.run(host='0.0.0.0')
