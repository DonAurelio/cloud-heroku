from celery import Celery
from processing import process_client_video

import os

app = Celery(
    'tasks', 
    backend='rpc://', 
    broker=os.environ.get('BROKER_URL','pyamqp://guest@localhost//')
)

@app.task
def hello_world():
    return "Hello World"

@app.task
def process_video(domain_url, video_id, input_file, output_file):
    domain_url = domain_url[0]
    video_id = video_id[0]
    input_file = input_file[0]
    return process_client_video(domain_url, video_id, input_file, output_file)