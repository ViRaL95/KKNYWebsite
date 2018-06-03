from SECRETS import secrets
import logging
import requests
import sys
from importlib import reload

class NewsConnection:
    """This class retrieves news from newsapi.org.
    ALL USERNAME AND PASSWORD NEEDED TO DEBUG ISSUES WITH THE NEWS API HAS BEEN SENT TO
    info@kkny.org

    Attributes:
        url (str): The url that this module will make requests to. Contains domain name, version number, newspaper and API KEY
        version_no (int): The API version no.
        newspaper (str): The newspaper we are retrieving articles from which is the-times-of-india
        api_key (str): Unique API Key used to retrieve news from https://newsapi.org.
        domain_name (str): The domain name of the API we are connecting to, which is https://newsapi.org
    """
    def __init__(self): 
        self.api_key = secrets.API_KEY
        self.domain_name = secrets.DOMAIN_NAME
        self.version_no = secrets.VERSION_NO
        self.newspaper = secrets.NEWSPAPER
        self.url = secrets.URL
        self.url = self.url.format(self.domain_name, self.version_no, self.newspaper, self.api_key)
   
    def retrieveNews(self):
        #A GET REQUEST PERFORMED IN ORDER TO RETRIEVE NEWS CONTENT. IF THE NEWSPAPER WOULD LIKE TO BE CHANGED PLEASE VIEW THE SECRETS MODULE IN THE SECRETS PACKAGE
        requestAllNewspapers = requests.get(self.url)
        #THE RESPONSE CODE SHOULD ALWAYS BE A 200 (SIGNIFYING EVERYTHING IS OKAY)
        response_code = requestAllNewspapers.status_code
        #WE ARE THEN RETURNING ARTICLES
        return requestAllNewspapers.json()["articles"]
