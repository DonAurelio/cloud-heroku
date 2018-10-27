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
        self.bucket = self.s3.Bucket('aucarvideobucket')

    def create_or_update_contest(self, company_name, contest_name, url, start_date, end_date, award_description, image=None, image_url='', update=False):

        if image:
            # Creating a key to store data into s3 bucket. 
            # each file in s3 must have unique key.
            image_key = uuid.uuid4().hex
            # Saving image into s3 bucket
            self.bucket.upload_fileobj(Fileobj=image.file,Key=image_key)
            # Giving acces permissions to images 
            object_acl = self.s3.ObjectAcl('aucarvideobucket', image_key)
            response = object_acl.put(ACL='public-read')

            image_url = f'https://s3-us-west-2.amazonaws.com/aucarvideobucket/{image_key}' 

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

        # If we are performing an create operation we check for no repeated 
        # contest names
        if not update:
            # Does not allow repeated Contests names
            kwargs['ConditionExpression'] = "attribute_not_exists(Contests.#new_contest)"
        try:
            response = self.table_companies.update_item(**kwargs)

            # for every contest, we create a video repository (Dynamo Table)
            response = self.table_contest_videos.put_item(
              Item={
                  'Company': company_name,
                  'Contest': contest_name,
                  'Videos': {}
              }
            )
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                raise Exception(f'El concurso \'{contest_name}\' ya existe.')
            else:
                raise Exception('No es posible insertar datos en DynamoDB.')

        return response.get('ResponseMetadata').get('HTTPStatusCode')

    def get_company_contests(self, company_name):
        # Bringing the company data
        print('company_name',company_name)
        try:
            response = self.table_companies.get_item(
                Key={
                    'Name': company_name,
                }
            )
        except botocore.exceptions.ClientError as e:
            print(e.response['Error']['Message'])
            return {}
        else:
            print(response)
            item = response['Item']
            data_str = json.dumps(item, indent=4)
            data_dic = json.loads(data_str)

        return data_dic

    def get_contest_by_url(self, company_name, contest_url):

        data = self.get_company_contests(company_name)
        contests = data.get('Contests',{})
        contest = None
        for contest_name, contest_data in contests.items():
            if contest_data.get('Url') == contest_url:
                contest = contest_name, contest_data

        return contest


class DynamoVideoManager(object):

    PROCESSING = 'Processing'
    CONVERTED = 'Converted'

    def __init__(self):
        # Dynamo resource
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        # Each company has a contest and each contest has a map of videos
        self.table_contest_videos = dynamodb.Table('ContestVideos')

    def create_video(self, company_name, contest_name, video_name, url, person_fname, person_lname, person_email ):

        # NOTE: we have to add an UUID to the video name to ensure the videos has unique identification
        status = PROCESSING
        uploaded_at = datetime.datetime.now()

        response = self.table_contest_videos.update_item(
            Key={
                'company': company_name,
                'contest': contest_name
            },
            UpdateExpression = "SET CompanyVideos.#new_video = :new_data",
            ExpressionAttributeNames = { 
                "#new_video" : video_name
            },
            ExpressionAttributeValues={
                ':new_data': {
                    'url': url,
                    'status': status,
                    'uploaded_at': uploaded_at,
                    'person_fname': person_fname,
                    'person_lname': person_lname,
                    'person_email': person_email,

                }
            },
            # Does not allow repeated Contests
            ConditionExpression = "attribute_not_exists(CompanyVideos.#new_video)"
        )

        return response.get('ResponseMetadata').get('HTTPStatusCode')

    def get_videos(self, company_name, contest_name):
        pass
