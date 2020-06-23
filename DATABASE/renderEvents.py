from pymongo import MongoClient


class Events:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.database = self.client.KKNY

    def retrieve_events(self):
        event_names = self.database['event_names']
        return event_names.find({}) 
