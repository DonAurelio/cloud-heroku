from django.db import models
from django.contrib.auth.models import User

import boto3
import botocore
import json
import uuid


company_name = models.CharField(max_length=32, unique=True, null=True)
company_name.contribute_to_class(User, 'company_name')


class DynamoCompanyManager(object):

    def __init__(self):
        # Dynamo resource
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        # Company Table
        self.table_companies = dynamodb.Table('Companies')

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
