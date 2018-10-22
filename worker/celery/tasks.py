from celery import Celery
from processing import process_client_video

import os
import urllib
import logging


logging.basicConfig(
    format='%(levelname)s : %(asctime)s : %(message)s',
    level=logging.DEBUG
)

# To print loggin information in the console
logging.getLogger().addHandler(logging.StreamHandler())


# Celery app definition
app = None


# Configuration Documentation 
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#configuration

# Configuration for Rabbitmq
# backend: Use rabbitmq to store the resulsts.
# borker: Use rabitmq as broker.
#   example: pyamqp://<user>:<pass>@localhost:5672/<virtual-host>

if os.environ.get('BROKER_URL',''):
    logging.info('Rabbitmq broker selected')
    BROKER_URL = os.environ.get('BROKER_URL')

    app = Celery('tasks',
        backend='rpc://', 
        broker=BROKER_URL,
        task_default_queue='celery'
    )

# Configuration for AWS SQS
# backend: You can use AWS Dynamo a NoSQL database engine. To store results.
# borker: Use AWS SQS as broker.
#   example: sqs://aws_access_key_id:aws_secret_access_key@

if os.environ.get('AWS_ACCESS_KEY_ID',''):
    logging.info('AWS SQS broker selected')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID','')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY','')

    BROKER_URL = 'sqs://{0}:{1}@{2}'.format(
        # AWS_ACCESS_KEY_ID,
        urllib.parse.quote(AWS_ACCESS_KEY_ID, safe=''),
        # AWS_SECRET_ACCESS_KEY
        urllib.parse.quote(AWS_SECRET_ACCESS_KEY, safe=''),
        'sqs.us-west-2.amazonaws.com/660158453105/aucar-sqs-C-celery'
    )

    app = Celery('tasks',
        broker=BROKER_URL,
        result_backend=None,
        task_default_queue='aucar-sqs-C-celery',
        broker_transport_options={
            'region': 'us-west-2',
            'polling_interval': 20,
            'queue_name_prefix:': 'aucar-sqs-C-'
        }
    )


@app.task
def hello_world():
    return "Hello World"

@app.task
def process_video(video_id, input_file, output_file):
    return process_client_video(video_id, input_file, output_file)