from pymongo import MongoClient


class CommitteeMembers:
    """This class retrieves all members of each individual committee. Each method retrieves
    the members from different committees.

    If one were to want to create a new committee they would have to go to the database
    and create a new collection. One can create a new collection my accessing the mongo shell.

    One should then create a method below which will access the correct collection. One should
    follow the format of the previous methods written below
    """
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.database = self.client.KKNY

    def retrieveContactsList(self):
        contact_list = self.database['contact_list']
        return contact_list.find({})

    def retrieveExecutiveCommittee(self):
        executive_committee = self.database['executive_committee']
        return executive_committee.find({})

    def retrieveCulturalCommittee(self):
        cultural_committee = self.database['cultural_committee']
        return cultural_committee.find({})

    def retrieveYouthCommittee(self):
        youth_committee = self.database['youth_committee']
        return youth_committee.find({})

    def retrieveFoodCommittee(self):
        food_committee = self.database['food_committee']
        return food_committee.find({})

    def retrieveFundraisingCommittee(self):
        fundraising_committee = self.database['fundraising_committee']
        return fundraising_committee.find({})

    def retrieveSoundMusicCommittee(self):
        sound_music_committee = self.database['sound_music_system']
        return sound_music_committee.find({})

    def retrieveDecorationsCommittee(self):
        decorations_committee = self.database['decorations_committee']
        return decorations_committee.find({})

    def retrieveSportsCommittee(self):
        sports_committee = self.database['sports_collection']
        return sports_committee.find({})

    def retrievePreviousCommittee(self):
        previous_committee = self.database['previous_committee']
        return previous_committee.find({})

