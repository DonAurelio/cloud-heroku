# -*- coding: utf-8 -*-

import requests
import datetime
import logging
import sys
import subprocess
import os
import boto3
import tempfile
import time


logging.basicConfig(
    format='%(levelname)s : %(asctime)s : %(message)s',
    level=logging.DEBUG
)

# To print loggin information in the console
logging.getLogger().addHandler(logging.StreamHandler())

# The directory which contains this file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The path to the nfs directory on which media to be processed will reside
#NFS_PATH = os.environ.get('NFS_PATH','/home/app/nfs')

# The IP and PORT of the WebService
WEB_IP = os.environ.get('WEB_IP')
WEB_PORT = os.environ.get('WEB_PORT')

# The endpoint URL to send the notification when a video has been processed successfully
CLIENT_VIDEO_STATUS_URL = f"http://{WEB_IP}:{WEB_PORT}/api/contest/videos/status/"

S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')

#WORKER_TIME_FILE_PATH = os.environ.get('WORKER_TIME_FILE_PATH','.')

# Print the values of the varuables
status = 'Running with settings' + '\n'
#status += 'NFS_PATH:' + '\t' + NFS_PATH + '\n'
status += 'WEB_IP:' + '\t' + WEB_IP + '\n'
status += 'WEB_PORT:' + '\t' + WEB_PORT + '\n'
status += 'WEB_VIDEO_STAT_ENPOINT:' + '\t' + CLIENT_VIDEO_STATUS_URL + '\n'
#status += 'WORKER_TIME_FILE_PATH' + '\t' + WORKER_TIME_FILE_PATH

logging.info(status)




#def timer(func):
    #"""
        #Measures the execution time of the decorated
        #function and place the resuts in a .log file
    #"""
    #def wrapper(*args):
        #start = time.perf_counter()
        #code, out, err = func(*args)
        #end = time.perf_counter()

        #  Save the time in miliseconds, the video processing
        #  status code, input and output files path.
        #text = f'{end-start}\t{args[0]}\t{args[1]}\n'
        #logging.info(text)
        #with open(WORKER_TIME_FILE_PATH,'a+') as file:
        #    file.write(text)


        #return code, out, err

    #return wrapper


# @timer
def process_video(input_file, output_file):
    """
        Process a video located at input_file path
        and place the processed video in output_file
        path

        input_file (str): Path to the file to be processed,
            example: /media/contests/videos/rihana.avi.

        output_file (str): Path to the processed file,
            example: /media/contests/videos/rihana_converted.mp4.
    """

    exists = os.path.isfile(output_file)
    if exists:
        # If the files already exists.
        # it is not necessary to perform
        # processing again
        return 0, None, None

    logging.info(f'Start processing {input_file} to {output_file}')

    #  Take time of video processing step
    
    command = f'ffmpeg -i {input_file} {output_file}'
    
    process = subprocess.run(
        args=command,
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        shell=True, 
        universal_newlines=True,
    )

    success = 0
    code = process.returncode
    out = process.stdout
    err = process.stderr

    if code == success:
        # Video processing was converted correctly
        logging.info(f'End processing file {input_file}')
    else:
        # An erro has ocurred during videos processing
        logging.error(f'{out} {err} {input_file}')

    return process.returncode, process.stdout, process.stderr


def notify_client(company_name,contest_name,video_name,video_id,web_url,email_rcv):
    """
        Notify to a client that a video has been processed
        succesfully.

        video_id (int): The id of the video being processed.
    """

    response = requests.post(
        url=CLIENT_VIDEO_STATUS_URL, 
        data= {
            'company_name': company_name,
            'contest_name': contest_name,
            'video_name': video_name,
            'web_url':web_url,
            'video_id':video_id,
            'email_rcv': email_rcv
        }
    )

    if response.status_code == 200:
        logging.info(f'Notification sended for video {video_id}')
    else:
        logging.error(f'Notification error for videos {video_id}')


def process_s3_video(company_name,contest_name,video_name,video_id,web_url,email_rcv):

    video_ext = video_name.split('.')[-1]
    input_file = video_id + '.' + video_ext
    output_file = video_id + '.mp4'

    logging.info(f'Selecting {S3_BUCKET_NAME} bucket')
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(S3_BUCKET_NAME)

    with tempfile.TemporaryDirectory() as dir_path:
        input_file_path = os.path.join(dir_path,input_file)
        output_file_path = os.path.join(dir_path,output_file)

        logging.info(f'Downloading {video_id} in bucket to {input_file_path}')
        bucket.download_file(video_id,input_file_path)

        code, out, err = process_video(input_file_path,output_file_path)
        success = 0
        if code == success:
            logging.info(f'Process success {input_file_path}')

            logging.info(f'Uploading {output_file_path} in bucket {S3_BUCKET_NAME}')
            bucket_file_name = video_id + '_converted'
            bucket.upload_file(output_file_path, bucket_file_name)

            # Giving acces permissions to images 
            object_acl = s3.ObjectAcl(S3_BUCKET_NAME, bucket_file_name)
            response = object_acl.put(ACL='public-read')

            notify_client(company_name,contest_name,video_name,video_id,web_url,email_rcv)
            return code
           
        logging.error(f'{out} {err} {input_file_path}')
        return code