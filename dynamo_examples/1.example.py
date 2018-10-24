# SDK for Python to perform operations on AWS DynamoDB 
import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Create the DynamoDB table.
contest_table = dynamodb.create_table(
    TableName='contests',
    # Compound primary key
    KeySchema=[
    	# The company that ofers the competition
        {
            'AttributeName': 'company_name',
            'KeyType': 'HASH'
        },
        # Name of the competition
        {
            'AttributeName': 'name',
            'KeyType': 'S'
        },
    ],
    AttributeDefinitions=[
    	# Contest unique URL
        {
            'AttributeName': 'url',
            'AttributeType': 'S'
        },
        # Constest image S3 URL
        {
            'AttributeName': 'banner',
            'AttributeType': 'S'
        },
        # Contest start date
        {
            'AttributeName': 'start_date',
            'AttributeType': 'S'
        },
        # Contest end date
        {
            'AttributeName': 'end_date',
            'AttributeType': 'S'
        },
        # Contest winner award description
        {
            'AttributeName': 'award_description',
            'AttributeType': 'S'
        },
    ],
    ProvisionedThroughput={
    	'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists.
contest_table.meta.client.get_waiter('table_exists').wait(TableName='contests')

# Print out some data about the table.
print(contest_table.item_count)


# Create the DynamoDB table.
participant_table = dynamodb.create_table(
    TableName='participant',
    # Compound primary key
    KeySchema=[
        {
            'AttributeName': 'first_name',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'last_name',
            'KeyType': 'RANGE'
        },
    ],
    AttributeDefinitions=[
    	# Participant email
        {
            'AttributeName': 'email',
            'AttributeType': 'S'
        },
    ],
    ProvisionedThroughput={
    	'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists.
participant_table.meta.client.get_waiter('table_exists').wait(TableName='participant')

# Print out some data about the table.
print(participant_table.item_count)


# Create the DynamoDB table.
video_table = dynamodb.create_table(
    TableName='videos',
    # Simple primary key
    KeySchema=[
        {
        	# Video S3 URL
            'AttributeName': 'url',
            'KeyType': 'HASH'
        },
    ],
    AttributeDefinitions=[
        # Name of the competition
        {
            'AttributeName': 'contest',
            'AttributeType': 'S'
        },
        # Constest image URL
        {
            'AttributeName': 'banner',
            'AttributeType': 'S'
        },
        # Contest start date
        {
            'AttributeName': 'start_date',
            'AttributeType': 'S'
        },
        # Contest end date
        {
            'AttributeName': 'end_date',
            'AttributeType': 'S'
        },
        # Contest winner award description
        {
            'AttributeName': 'award_description',
            'AttributeType': 'S'
        },
    ],
    ProvisionedThroughput={
    	'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists.
video_table.meta.client.get_waiter('table_exists').wait(TableName='videos')

# Print out some data about the table.
print(video_table.item_count)
