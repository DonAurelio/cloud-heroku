from django import forms

import datetime
import boto3
import botocore


class DynamoContestManager(object):

    def __init__(self):
        # Dynamo resource
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        # Company Table
        self.table_companies = dynamodb.Table('Companies')
        # Each company has a contest and each contest has a map of videos
        self.table_contest_videos = dynamodb.Table('ContestVideos')

    def create_contest(self, company_name, contest_name, url, image_url, start_date, end_date, award_description ):

        # We add a new contest the company contests map
        response = self.table_companies.update_item(
            Key={
                'name': company_name
            },
            UpdateExpression = "SET Contests.#new_contest = :new_data",
            ExpressionAttributeNames = { 
                "#new_contest" : contest_name
            },
            ExpressionAttributeValues={
                ':new_data': {
                    'url': url,
                    'image_url': image_url,
                    'start_date': start_date,
                    'end_date': end_date,
                    'award_description': award_description
                }
            },
            # Does not allow repeated Contests
            ConditionExpression = "attribute_not_exists(Contests.#new_contest)"
        )

        # for every contest we create a video repository (Dynamo Table)
        response = self.table_contest_videos.put_item(
          Item={
              'company': company_name,
              'contest': contest_name,
              'contest': {}
          }
        )

        return response.get('ResponseMetadata').get('HTTPStatusCode')

    def get_company_contests(self, company_name):
        # Bringing the company data
        try:
            response = table_companies.get_item(
                Key={
                    'company': company_name,
                }
            )
        except botocore.exceptions.ClientError as e:
            print(e.response['Error']['Message'])
            return {}
        else:
            item = response['Item']
            print("GetItem succeeded:")
            data_str = json.dumps(item, indent=4)
            data_dic = json.loads(data_str)
            print(data_dic)
            print(type(data_dic))

        return data_dic


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
