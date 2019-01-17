from pymongo import MongoClient
import json

class Login:
    def __init__(self, user_info):
        self.client = MongoClient('localhost', 27017) 
        self.database = self.client.KKNY
        self.user_info = user_info
        self.collection = self.database["users"]

    def verify_user_exists(self):
        self.email = self.user_info["email"]
        self.password = self.user_info["password"]
        num_users_that_exist = self.collection.find({"email": self.email, "password": self.password}).count()

        if num_users_that_exist == 1:
            return json.dumps({"user_exists": True})
        return json.dumps({"user_exists": False})
    
    #def is_active(self):

    #def is_anonymous(self):
     
    #get_id(self)
   
        
