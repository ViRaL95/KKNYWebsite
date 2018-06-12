from API.newsConnection import NewsConnection
from EMAIL import emailKKNYInfo 
from DATABASE.renderMembers import CommitteeMembers
import json
from flask import Flask, render_template, request
application = Flask(__name__)

"""
HTML Files are in the templates directory
homepage.html is rendered with news articles. The news articles are recieved from the newsConnection module in the API Package.
"""
@application.route("/")
def start():
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
    return render_template('presidents_message.html')

@application.route("/sendSuggestionToSuggestionsBox", methods=['POST'])
def sendEmail():
    suggestion = request.get_json()
    emailKKNYInfo.email_kkny_account(suggestion)
    return "success"

if __name__ == "__main__":
    application.run(host='0.0.0.0')
