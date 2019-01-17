import boto3
import shutil
import os
import sys
sys.path.insert(0, '/home/KKNY/KKNY_Website_Production_Environment/DATABASE')
from retrieve_event_for_photo_gallery import PreviousEvents

ACCESS_KEY = 'AKIAJW7PRZDO57ND665A'
AWS_SECRET_KEY ='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'
previous_events = PreviousEvents()
event_info = previous_events.retrieve_event_info(event_name=sys.argv[1]) 
session = boto3.Session(aws_access_key_id=ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
s3 = session.resource('s3')
directory = "/home/KKNY/KKNY_Website_Production_Environment/static/" + event_info[0]["photo_directory"]
if os.path.exists(directory):
    shutil.rmtree(directory)
if not os.path.exists(directory):
    os.mkdir(directory)
    bucket = s3.Bucket(name=event_info[0]["bucket"])
    for file_ in bucket.objects.all():
        print(event_info[0]["photo_directory"] + "/" + file_.key)
        bucket.download_file(file_.key, directory + "/" + file_.key)
	
