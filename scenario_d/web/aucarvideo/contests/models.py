from django import forms

import datetime
import boto3
import botocore


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
