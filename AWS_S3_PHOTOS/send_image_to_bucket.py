import boto3
import uuid
import datetime
import sys
sys.path.insert(0, '/home/KKNY/KKNY_Website_Production_Environment')
from SECRETS import secrets

class Photo_Send_s3:
    def __init__(self):
        self.access_key = secrets.AWS_ACCESS_KEY
        self.AWSSecretKey = secrets.AWS_SECRET_KEY
        self.allowed_image_extensions = ["png", "jpg", "jpeg", "gif"]

    def send_photo_to_s3(self, photos, user_info, event_info):
        session = boto3.Session(aws_access_key_id=self.access_key, aws_secret_access_key=self.AWSSecretKey)
        s3 = session.client('s3')
        for photo in photos:
            #Ensure that the image contains an extension
            if "." not in photo.filename:
                return {"success": False, "message": "Please only include images with extensions"}
            #Get extension from filename provided by user. extension SHOULD BE .png, .jpg, .jpeg, or .gif
            image_extension = photo.filename.split(".")[-1]
            if image_extension.lower() not in self.allowed_image_extensions:
                return {"success": False, "message": "Please only include images with .png, .jpg, .jpeg or .gif extension"}
            #Generate a random file name. Why generate a random file name? What if two users submit two different images with the same file name? S3 will remove the first image.
            random_file_name = str(uuid.uuid4())

            #Store image in AWS along with email address metadata of the user who sent the photo. 
            s3.put_object(Body=photo.stream, Bucket=event_info[0]["bucket"], Key=random_file_name + "." + image_extension)
        return {"success": True, "message": "Your photos have been successfully uploaded. After review, the photos should be included in the KKNY photo gallery"}
