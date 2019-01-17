import pymongo
from pymongo import MongoClient

class PreviousEvents:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.database = self.client.KKNY

    def retrieve_event_info(self, event_name=None, event_id=None):
        """ 
        This method retrievs the event name, and the        respective directory where photos are stored        .
        """
        event_names = self.database['past_events']
        if event_id:
            return event_names.find({"event_id": event_id})
        return event_names.find({"event_name": event_name})
   
    def retrieve_all_event_info(self):
        """
        This method retrieves all events and their respective information
        """
        all_events = self.database['past_events']
        return all_events.find({}).sort("event_id",pymongo.DESCENDING)
