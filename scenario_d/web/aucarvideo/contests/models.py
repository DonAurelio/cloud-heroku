from django.conf import settings

import datetime
import boto3
import botocore
import uuid
import logging
import json


# Get an instance of a logger
logger = logging.getLogger(__name__)


class DynamoContestManager(object):

    def __init__(self):
        # Dynamo resource
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

        # Company Table
        self.table_companies = dynamodb.Table('Companies')

        # Each company has a contest and each contest has a map of videos
        self.table_contest_videos = dynamodb.Table('ContestVideos')

        # S3 resouce
        self.s3 = boto3.resource('s3')
        self.bucket = self.s3.Bucket(settings.S3_BUCKET_NAME)

    def add_object_to_bucket(self, file_obj):
        # Creating a key to store data into s3 bucket. 
        # each file in s3 must have unique key.
        obj_key = uuid.uuid4().hex

        self.bucket.upload_fileobj(Fileobj=file_obj, Key=obj_key)
        
        # Giving acces permissions to images 
        object_acl = self.s3.ObjectAcl(settings.S3_BUCKET_NAME, obj_key)
        response = object_acl.put(ACL='public-read')

        return obj_key, settings.FRONT_CONTENT_URL_FORMAT.format(s3_obj_key=obj_key)

    def delete_object_from_bucket(self,obj_url):
        obj_key = obj_url.split('/')[-1]

        response = self.bucket.delete_objects(
            Delete={
                'Objects': [
                    {
                        'Key': obj_key,
                    },
                ],
                'Quiet': False
            },
            MFA='string',
            RequestPayer='requester'
        )

        return response.get('ResponseMetadata').get('HTTPStatusCode')

    def create_contest(self, company_name, contest_name, image, url, start_date, end_date, award_description):

        obj_key, image_url = self.add_object_to_bucket(image.file)

        # Creating the new contest inside the company map 
        contest_kwargs = {
            'Key':{
                'Name': company_name
            },
            'UpdateExpression':"SET Contests.#new_contest = :new_data",
            'ExpressionAttributeNames': { 
                "#new_contest" : contest_name
            },
            'ExpressionAttributeValues':{
                ':new_data': {
                    'Url': url,
                    'Image_url': image_url,
                    'Start_date': str(start_date),
                    'End_date': str(end_date),
                    'Award_description': award_description
                }
            },
            # If the contest already exists it will raise and exeption
            'ConditionExpression': "attribute_not_exists(Contests.#new_contest)"
        }

        # Creating the contest videos repository (dynamo table) as empty
        videos_table_kwargs = {              
            'Item':{
              'Company': company_name,
              'Contest': contest_name,
              'Videos': {}
            }
        }

        try:

            response = self.table_companies.update_item(**contest_kwargs)
            response = self.table_contest_videos.put_item(**videos_table_kwargs)

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                raise Exception(f'El concurso \'{contest_name}\' ya existe.')
            else:
                raise Exception('No es posible insertar datos en DynamoDB.')

        return response.get('ResponseMetadata').get('HTTPStatusCode')

    def update_contest(self, company_name, contest_name, new_image, image_url, url, start_date, end_date, award_description):

        assert image_url, 'image_url must be provided!'
        
        if new_image and image_url:
            self.delete_object_from_bucket(image_url)
            obj_key, image_url = self.add_object_to_bucket(image.file)

        # Creating the new contest inside the company map 
        kwargs = {
            'Key':{
                'Name': company_name
            },
            'UpdateExpression':"SET Contests.#new_contest = :new_data",
            'ExpressionAttributeNames': { 
                "#new_contest" : contest_name
            },
            'ExpressionAttributeValues':{
                ':new_data': {
                    'Url': url,
                    'Image_url': image_url,
                    'Start_date': str(start_date),
                    'End_date': str(end_date),
                    'Award_description': award_description
                }
            },

        }

        try:
            response = self.table_companies.update_item(**kwargs)

        except botocore.exceptions.ClientError as e:
            raise Exception('No es posible insertar datos en DynamoDB.')

        return response.get('ResponseMetadata').get('HTTPStatusCode')

    def get_contests(self, company_name):
        # Bringing the company data
        try:
            response = self.table_companies.get_item(
                Key={
                    'Name': company_name,
                }
            )
        except botocore.exceptions.ClientError as e:
            return {}
        else:
            item = response['Item']
            data_str = json.dumps(item, indent=4)
            data_dic = json.loads(data_str)

        return data_dic

    def get_contest_by_url(self, company_name, contest_url):

        data = self.get_contests(company_name)
        contests = data.get('Contests',{})
        contest = None
        for contest_name, contest_data in contests.items():
            if contest_data.get('Url') == contest_url:
                contest = contest_name, contest_data

        return contest

    def delete_contest_by_url(self, company_name, contest_url):

        contest_name, contest_data = self.get_contest_by_url(company_name, contest_url)

        # Creating the new contest inside the company map 
        kwargs = {
            'Key':{
                'Name': company_name
            },
            'UpdateExpression':"REMOVE Contests.#contest",
            'ExpressionAttributeNames': { 
                "#contest" : contest_name
            }
        }

        response = self.table_companies.update_item(**kwargs)

        return response.get('ResponseMetadata').get('HTTPStatusCode')


class DynamoVideoManager(object):

    def __init__(self):
        # Dynamo resource
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        # Each company has a contest and each contest has a map of videos
        self.table_contest_videos = dynamodb.Table('ContestVideos')
        # S3 resouce
        self.s3 = boto3.resource('s3')
        self.bucket = self.s3.Bucket(settings.S3_BUCKET_NAME)

    def add_object_to_bucket(self, file_obj):
        # Creating a key to store data into s3 bucket. 
        # each file in s3 must have unique key.
        obj_key = uuid.uuid4().hex

        self.bucket.upload_fileobj(Fileobj=file_obj,Key=obj_key)
        
        # Giving acces permissions to images 
        object_acl = self.s3.ObjectAcl(settings.S3_BUCKET_NAME, obj_key)
        response = object_acl.put(ACL='public-read')

        return obj_key, settings.FRONT_CONTENT_URL_FORMAT.format(s3_obj_key=obj_key)

    def delete_object_from_bucket(self,obj_url):
        obj_key = obj_url.split('/')[-1]

        response = self.bucket.delete_objects(
            Delete={
                'Objects': [
                    {
                        'Key': obj_key,
                    },
                ],
                'Quiet': False
            },
            MFA='string',
            RequestPayer='requester'
        )

        return response.get('ResponseMetadata').get('HTTPStatusCode')

    def create_video(self, company_name, contest_name, video, description, uploaded_at, status, p_fname, p_lname, p_email):

        obj_key, video_url = self.add_object_to_bucket(video.file)

        kwargs = {
            'Key': {
                'Company': company_name,
                'Contest': contest_name
            },
            'UpdateExpression': "SET Videos.#new_video = :new_data",
            'ExpressionAttributeNames': { 
                "#new_video" : obj_key
            },
            'ExpressionAttributeValues':{
                ':new_data': {
                    'Name': video.name,
                    'Url': video_url,
                    'Description': description,
                    'Uploaded_at': uploaded_at,
                    'Status': status,
                    'Person_fname': p_fname,
                    'Person_lname': p_lname,
                    'Person_email': p_email,
                }
            }
        }

        # try:
        response = self.table_contest_videos.update_item(**kwargs)
        status = response.get('ResponseMetadata').get('HTTPStatusCode')
        # except botocore.exceptions.ClientError as e:
        #     raise Exception('No es posible insertar datos en DynamoDB.')

        return obj_key, status

    def delete_video_by_url(self, company_name, contest_name, video_url):

        contest_name, contest_data = self.get_contest_by_url(company_name, contest_url)

        # Creating the new contest inside the company map 
        kwargs = {
            'Key':{
                'Name': company_name
            },
            'UpdateExpression':"REMOVE Contests.#contest",
            'ExpressionAttributeNames': { 
                "#contest" : contest_name
            }
        }

        response = self.table_companies.update_item(**kwargs)

        return response.get('ResponseMetadata').get('HTTPStatusCode')

    def get_videos(self, company_name, contest_name):
        try:
            response = self.table_contest_videos.get_item(
                Key={
                    'Company': company_name,
                    'Contest': contest_name
                }
            )
        except botocore.exceptions.ClientError as e:
            return {}
        else:
            item = response['Item']
            data_str = json.dumps(item, indent=4)
            data_dic = json.loads(data_str)

        return data_dic.get('Videos')

    def update_video_status(self, company_name, contest_name, video_id):

        kwargs = {
            'Key': {
                'Company': company_name,
                'Contest': contest_name
            },
            'UpdateExpression': "SET Videos.#video_id.Status = :new_data",
            'ExpressionAttributeNames': { 
                "#video_id" : video_id
            },
            'ExpressionAttributeValues':{
                ':new_data': 'Converted'
            }
        }


        response = self.table_contest_videos.update_item(**kwargs)
        status = response.get('ResponseMetadata').get('HTTPStatusCode')

        return status