# -*- coding: utf-8 -*-

import requests
import datetime
import logging
import sys
import subprocess
import os
import time
import multiprocessing


logging.basicConfig(
    format='%(levelname)s : %(asctime)s : %(message)s',
    level=logging.DEBUG
)

# To print loggin information in the console
logging.getLogger().addHandler(logging.StreamHandler())

# The directory which contains this file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The path to the nfs directory on which media to be processed will reside
NFS_PATH = os.environ.get('NFS_PATH','/home/app/nfs')

# The IP and PORT of the WebService
WEB_IP = os.environ.get('WEB_IP')
WEB_PORT = os.environ.get('WEB_PORT')

# The endpoint URL to send the notification when a video has been processed successfully
CLIENT_VIDEO_STATUS_URL = f"http://{WEB_IP}:{WEB_PORT}/api/contest/videos/status/"

# Print the values of the varuables
status = 'Running with settings' + '\n'
status += 'NFS_PATH:' + '\t' + NFS_PATH + '\n'
status += 'WEB_IP:' + '\t' + WEB_IP + '\n'
status += 'WEB_PORT:' + '\t' + WEB_PORT + '\n'
status += 'WEB_VIDEO_STAT_ENPOINT:' + '\t' + CLIENT_VIDEO_STATUS_URL

logging.info(status)


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

    # Remove the first '/media/' on the video path
    input_file = input_file[7:]
    output_file = output_file[7:]

    input_file = os.path.join(NFS_PATH,input_file)
    output_file = os.path.join(NFS_PATH,output_file)

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


def process_client_video(video_id, input_file, output_file):
    """
        Processes a video.

        video_data (list): Information of the video to be
            processed.

        Example:

            [
                # The ID of the video
                11,
                # The path to the video in the media folder
                "/media/contests/videos/Nelly_Furtado_-_Promiscuous_ft._Timbaland.avi",
                # The name of the converted version of the video.
                "/media/contests/videos/Nelly_Furtado_-_Promiscuous_ft._Timbaland_Converted.mp4"
            ]
    """
    
    code, out, err = process_video(input_file,output_file)
    success = 0
    if code == success:
        logging.info(f'Process success {input_file}')
        notify_client(video_id)
        return code
       
    logging.error(f'{out} {err} {input_file}')
    return code


def notify_client(video_id):
    """
        Notify to a client that a video has been processed
        succesfully.

        video_id (int): The id of the video being processed.
    """

    response = requests.post(
        url=CLIENT_VIDEO_STATUS_URL, 
        data= {'video_id':video_id}
    )

    if response.status_code == 200:
        logging.info(f'Notification sended for video {video_id}')
    else:
        logging.error(f'Notification error for videos {video_id}')
