from datetime import datetime
import requests
from pprint import pprint
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
from donors.paypal_donations import retrieve_donors
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


@application.route('/localHeroes')
def render_local_heros():
    return render_template('local_heroes.html')


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
    print("entered upload pictures page")
    previous_events = PreviousEvents()
    event_info = previous_events.retrieve_event_info(event_name=event_name)
    upload_to_s3 = Photo_Send_s3()
    list_of_files = request.files.getlist("file[]")
    print("yahuhhh")
    return json.dumps(upload_to_s3.send_photo_to_s3(list_of_files, {'email': current_user.email}, event_info))

@application.errorhandler(413)
def request_entity_too_large(error):
    print("too large")
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

@application.route('/zoom_events', methods=['GET'])
def render_zoom_events():
    return render_template('zoom_events.html') 
  
@application.route("/donate", methods=['GET'])
def donate():
    donors = retrieve_donors()
    """
    authorization_request = \
        requests.post("https://api.paypal.com/v1/oauth2/token", headers={"Accept": "application/json",
                                                                        "Accept-Language": "en_US"},
                     auth=("AZTjzrpOI3kszOnGUgX4jQVEF5qfaSbCXUERBsGMFT_QMn88ILsKTMLrmiH-d9dytpMtTPj0jOBl_ilS",
                           "EFMJ9CNMPVSpGgeSDmU2FZlRNmum2fG9afp9KdDKe1Peqwkcmz7c9_OU-h3zZD9wP0vDij_p4fHQgZ7S"),
                     data={"grant_type": "client_credentials"})

    token = authorization_request.json()['access_token']
    ia_header = {"Authorization": "Bearer {}".format(token), "Content-Type": "application/json"}

    start_date = datetime(2020, 5, 17)
    current_date  = datetime.now().date()
    start_date_str = datetime.strftime(start_date, '%Y-%m-%dT%H:%M:%SZ')
    current_date_str = datetime.strftime(current_date, '%Y-%m-%dT%H:%M:%SZ')

    answer = requests.get("https://api.paypal.com/v1/reporting/transactions", headers=ia_header,
                          params={"start_date": start_date_str, "end_date": current_date_str,
                                  "transaction_type": "T0013",
                                  "fields": "payer_info"})

    payment_info = {payer['payer_info']['payer_name']['alternate_full_name']: payer['transaction_info']['transaction_amount']['value']
                    for payer in answer.json()['transaction_details']}


    payment_info_sorted = []
    for user, amount in sorted(payment_info.items(), key=lambda item: float(item[1]), reverse=True):
        payment_info_sorted.append(user)
    """
    return render_template('donate.html', donors=donors)

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
