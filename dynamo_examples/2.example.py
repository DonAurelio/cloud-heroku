import boto3
import json
from botocore.exceptions import ClientError


# Get the service resource.
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

# Instantiate a table resource object without actually
# creating a DynamoDB table. Note that the attributes of this table
# are lazy-loaded: a request is not made nor are the attribute
# values populated until the attributes
# on the table resource are accessed or its load() method is called.
# table = dynamodb.Table('aucar.companies')
table_companies = dynamodb.Table('Companies')
table_contest_videos = dynamodb.Table('ContestVideos')

# Print out some data about the table.
# This will cause a request to be made to DynamoDB and its attribute
# values will be set based on the response.
print(table_companies.creation_date_time)


# Creating an Item
# Creates a new item, or replaces an old item with a new item.
# If an item that has the same primary key as the new item already 
# exists in the specified table, the new item completely replaces the existing item. 

# response = table_companies.put_item(
# 	Item={
# 		'Name': 'Facebook',
# 		'Contests': {
# 			'contest_1': {
# 				'name': 'contest_1',
# 			},
# 			'contest_1': {
# 				'name': 'contest_3'
# 			},
# 		}
# 	}
# )

# print('put_item_response',response)


# Append Contests
# response = table_companies.update_item(
# 	Key={
# 		'Name':'Facebook'
# 	},
# 	UpdateExpression = "SET Contests.#new_contest = :new_data",
# 	ExpressionAttributeNames = { 
# 		"#new_contest" : "contest_5" 
# 	},
# 	ExpressionAttributeValues={
# 		':new_data': {
# 			'name': 'contest_4'
# 		}
# 	},
# 	# Does not allow repeated Contests
# 	ConditionExpression = "attribute_not_exists(Contests.#new_contest)"
# )

# print('append_contests_response',response)


# Bringing the company data
try:
    response = table_companies.get_item(
        Key={
            'Name': 'Facebook'
        }
    )
except ClientError as e:
    print(e.response['Error']['Message'])
else:
    item = response['Item']
    print("GetItem succeeded:")
    data_str = json.dumps(item, indent=4)
    data_dic = json.loads(data_str)
    print(data_dic)
    print(type(data_dic))

    for contest_name, contest_data in data_dic.get('Contests').items():
    	print(contest_name)
    	print(contest_data)



# response = table_contest_videos.put_item(
# 	Item={
# 		'Name': 'contest_1',
# 		'Videos': {},
# 	}
	
# )


# Update Item 
# response = table.update_item(
# 	Key={
# 		'Name':'Facebook'
# 	},
# 	UpdateExpression='SET Contests = :val',
# 	ExpressionAttributeValues={
# 		':val': {
# 			'contest': {
# 				'name': 'contest_1',
# 			}
# 		}
# 	}
# )


# # Getting an Item
# response = table.get_item(
# 	Key={
# 		'name': 'this is an example'
# 	}
# )

# print('get_item_response',response)

# Update Item 
# response = table.update_item(
# 	Key={
# 		'name':'this is and example'
# 	},
# 	UpdateExpression='SET name = :val',
# 	ExpressionAttributeValues={
# 		':val': 'hello world'
# 	}
# )

# Output: Invalid UpdateExpression: Attribute name is a reserved keyword; reserved keyword: name
# Work arroung:

# response = table.update_item(
# 	Key={
# 		'name':'this is and example'
# 	},
# 	UpdateExpression='SET #company = :val',
# 	ExpressionAttributeValues={
# 		':val': 'hello world'
# 	},
# 	ExpressionAttributeNames={
# 		'#company': 'name'
# 	}
# )


# print('response_update_item', response)

# # Deleting an Item
# response = table.delete_item(
# 	Key={
# 		'name': 'hello',

# 	}
# )

# print('response_delete_non_existing_item',response)