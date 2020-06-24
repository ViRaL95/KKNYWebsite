from API.newsConnection import NewsConnection
from EMAIL import emailKKNYInfo
from DATABASE.retrieve_event_for_photo_gallery import PreviousEvents 
from DATABASE.renderMembers import CommitteeMembers
from AUTHENTICATION.authenticator import validate_and_login_user, Signup, Login
from AWS_S3_PHOTOS.send_image_to_bucket import Photo_Send_s3
import json
from donors.paypal_donations import retrieve_donors
from flask import Flask, url_for, render_template, request, redirect, session
from flask_login import logout_user, login_required, current_user
from exceptions import SignUpException, LoginException

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////database/users.db'
application.config['SECRET_KEY'] = 'kkny_secrets'


@application.route('/login', methods=['POST'])
def login_user():
    login = Login(request.get_json())

    try:
        login.validate_login()
        login.login_user()

    except LoginException as e:
        return json.dumps({
            'successful_login': False,
            'message': str(e)
        })

    login_response = {
        'successful_login': True
    }

    if 'url' in session:
        login_response.update(redirect_to=session['url'])

    return json.dumps(login_response)


@application.route("/sign_up", methods=['POST'])
def signup_user():

    sign_up = Signup(request.get_json())

    try:
        sign_up.validate_signup()
        sign_up.signup_user()

    except SignUpException as e:
        return json.dumps({
            'successful_signup': False,
            'message': str(e)
        })

    return json.dumps({
        'successful_signup': True,
    })


@application.route("/")
def start():
    session.pop('url', None)
    newsConnection = NewsConnection()
    return render_template('homepage.html', news_articles=newsConnection.retrieveNews())


@application.route("/about")
def renderAboutUs():
    committeeMembers = CommitteeMembers()
    previous_committee = committeeMembers.retrievePreviousCommittee()
    return render_template('about.html', previous_committee=previous_committee);


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


@application.route('/local_heroes')
def render_local_heros():
    volunteer_group_one = [
	'Kavya (Coordinator)',
	'Keshav (Coordinator)',
	'Radhika',
	'Ravi',
	'Geetha',
	'Savitha Navada',
	'Gopal Navada',
	'Yeshoda',
	'Prakash Bhat',
	'Pranav Bhat',
	'Pushpalatha Bhat',
	'Danika',
	'Vittal',
	'',
	'',
	'',
	'',
	'',
	'',
	''
    ]
    volunteer_group_two = [
	'Nagini (Coordinator)',
	'Uma Sharath (Coordinator)',
	'Ravindra',
	'Aditya',
	'Sonika',
	'Sharath Kengeri',
	'Pragna',
	'Gopal',
	'Achala',
	'Purushotam',
	'Swaroop Kumble',
	'Hamsini Kumble',
	'Ojas',
	'Arun Kumar',
	'Geetha Kumar',
	'Ankith kumar',
	'Hrishikesh Deshpande',
	'Vasumathi',
        '',
        '',
        ''
    ]
    volunteer_group_three = [
	'Ajit Ganesh (Co-ordinator)',
	'Shilpa (Co-ordinator)',
	'Ajith Shetty',
	'Mahesh',
	'Ram',
	'Jyothi Babureddy',
	'Babu Reddy',
	'Veena',
	'Subha',
	'Anand',
	'Chaitra',
	'Sreeranjini',
	'Arya',
	'Ansh',
	'Shivkumar',
	'Ravindra Kudur',
	'Narsi Motagan',
	'Anitha',
	'Ram Marakula',
	'Sudha Marakula'
    ]
    volunteer_group_four = [
	'Triveni  (Coordinator)',
	'Raviteja  (Coordinator)',
	'Badari Ambati (Coordinator)',
	'Shreya Ambati',
	'Vinaya',
	'Aiysha',
	'Ankush',
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	''
    ]
    return render_template('local_heroes.html', volunteers=zip(volunteer_group_one, volunteer_group_two, volunteer_group_three, volunteer_group_four))


@application.route("/presidents_message")
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


@application.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("start"))
 
@application.route("/sign_up_page")
def signup_page():
    return render_template("sign_up.html")

@application.route('/zoom_events', methods=['GET'])
def render_zoom_events():
    return render_template('zoom_events.html') 
  

@application.route("/donate", methods=['GET'])
def donate():
    donors = retrieve_donors()
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
