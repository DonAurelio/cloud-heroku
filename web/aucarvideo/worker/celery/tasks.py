from celery import Celery
from processing import process_video

import os

app = Celery(
	'tasks', 
	backend='rpc://', 
	broker=os.environ.get('CELERY_BROKER_URL','')
)

@app.task
def task_process_video(domain_url, video_id, input_file, output_file):
	return process_client_video(domain_url, video_id, input_file, output_file)