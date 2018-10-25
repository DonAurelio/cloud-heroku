from django.db import models
from django.contrib.auth.models import User

import boto3
import botocore
import json


company_name = models.CharField(max_length=32, unique=True, null=True)
company_name.contribute_to_class(User, 'company_name')


class DynamoCompanyManager(object):

    def __init__(self):
        # Dynamo resource
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        # Company Table
        self.table_companies = dynamodb.Table('Companies')
        # Each company has a contest and each contest has a map of videos
        self.table_contest_videos = dynamodb.Table('ContestVideos')

    def create_company(self, company_name):
        # Creates a company item in dynamodb
        # If a company is placed with the same name i
        # it will be replaced
        response = self.table_companies.put_item(
          Item={
              'Name': company_name,
              'Contests': {}
          }
        )

        return response.get('ResponseMetadata').get('HTTPStatusCode')

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

    def get_company(self, company_name):
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
            item = response['Item']
            data_str = json.dumps(item, indent=4)
            data_dic = json.loads(data_str)

        return data_dic