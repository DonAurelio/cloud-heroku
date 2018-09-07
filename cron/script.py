#!/usr/local/bin/python3.6
# -*- coding: utf-8 -*-

import requests
import datetime
import logging
import sys
import subprocess
import os
import time
import multiprocessing

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_PATH = os.path.join(BASE_DIR, 'aucarvideo/media')


logging.basicConfig(
    format='%(levelname)s : %(asctime)s : %(message)s',
    level=logging.DEBUG
)

# To print loggin information in the console
logging.getLogger().addHandler(logging.StreamHandler())


# WEB_PUBLIC_URL = os.environ.get('WEB_PUBLIC_URL')
# MEDIA_PATH = os.environ.get('MEDIA_PATH')
# HOST_NAME = os.environ.get('HOST_NAME')
# PORT =os.environ.get('PORT')

WEB_PUBLIC_URL = 'aucarvideo.com'
MEDIA_PATH = sys.argv[1] if len(sys.argv) > 1 else ''
HOST_NAME = sys.argv[2] if len(sys.argv) > 2 else 'localhost'
PORT = sys.argv[3] if len(sys.argv) > 3 else '8000'

LOG_FILE_PATH =  sys.argv[4] if len(sys.argv) > 4 else './time.log'
CLIENTS_LIST_URL = f'http://{HOST_NAME}:{PORT}/api/client/list'
CLIENT_VIDEO_STATUS_URL = f'http://{HOST_NAME}:{PORT}/api/contest/videos/status/'

# Print the values of the varuables
status = 'Running with settings' + '\n'
status += 'WEB_PUBLIC_URL:' + WEB_PUBLIC_URL + '\n'
status += 'MEDIA_PATH:' + MEDIA_PATH + '\n'
status += 'HOST_NAME:' + HOST_NAME + '\n'
status += 'PORT:' + PORT + '\n'
status += 'LOG_FILE_PATH:' + LOG_FILE_PATH + '\n'
status += 'CLIENTS_LIST_URL:' + CLIENTS_LIST_URL + '\n'
status += 'CLIENT_VIDEO_STATUS_URL:' + CLIENT_VIDEO_STATUS_URL

logging.info(status)
lock = multiprocessing.Lock()

def get_clients_urls():
    """
    Return the home url of each tenant (client)
    created on the web application.
    """

    response = requests.get(
        # Requesting to the nginx host to send the
        # the urls of each tennat create on the web app
        url=CLIENTS_LIST_URL,

        # Whe inset the aucarvideo.com as host header on the
        # request so the django application can determine 
        # the tenent that will serve the request.
        headers={'host':WEB_PUBLIC_URL}
    )

    return response.json() if response.status_code == 200 else []


def get_client_videos_info(domain_url):
    """
        Return the paths of the videos uploaded by users to
        a certain client site. Sites in the SaaS application 
        can be: facebook.aucarvideo.com, monsters.aucarvideo.com,
        etc.

        For each site in the SaaS app. we request the path of the 
        videos uloaded by users. 

        domain_url (str): is the client home url without path,
            example: facebook.aucarvideo.com.
    """

    response = requests.get(
        url=CLIENT_VIDEO_STATUS_URL, 
        headers={'host':domain_url}
    )

    return response.json() if response.status_code == 200 else []


def get_videos_to_be_processed():
    """
    Return a list of information of every video that needs to 
    be processed from all clients (tenants) in the SaaS.

    Example:
        Every video data on the list contains the client domain URL,
        the ID of the video to be processed, the LOCATION of the 
        video in the media folder, and the name that will be assigned 
        to the processed version of the video.
        [
            [
                "facebook.aucarvideo.com",
                11,
                "/media/contests/videos/Nelly_Furtado_-_Promiscuous_ft._Timbaland.avi",
                "/media/contests/videos/Nelly_Furtado_-_Promiscuous_ft._Timbaland_Converted.mp4"
            ],
            [
                "whatsapp.aucarvideo.com",
                11,
                "/media/contests/videos/Nelly_Furtado_-_Promiscuous_ft._Timbaland.avi",
                "/media/contests/videos/Nelly_Furtado_-_Promiscuous_ft._Timbaland_Converted.mp4"
            ],

        ] 
    """
    clients_urls = get_clients_urls()
    # For every client url we resques a lis of videos
    # that needs to be processed

    videos_info = []
    for client_url in clients_urls:
        videos_info += get_client_videos_info(client_url)

    return videos_info


def timer(func):
    """
        Measures the execution time of the decorated 
        function and place the resuts in a .log file
    """
    def wrapper(*args):
        start = time.perf_counter()
        code, out, err = func(*args)
        end = time.perf_counter()

        #  Save the time in miliseconds, the video processing
        #  status code, input and output files path.
        
        with lock:
            with open(LOG_FILE_PATH,'a+') as file:
                input_file_path = os.path.join(MEDIA_PATH,args[0][1:])
                file_size = os.path.getsize(input_file_path)
                text = f'{end-start}\t{code}\t{file_size}\t{args[0]}\t{args[1]}\n'
                logging.info(text)
                file.write(text)


        return code, out, err

    return wrapper


@timer
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

    # Remove the first '/' on the video path
    input_file = input_file[1:]
    output_file = output_file[1:]

    input_file = os.path.join(MEDIA_PATH,input_file)
    output_file = os.path.join(MEDIA_PATH,output_file)

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


def process_client_video(video_data):
    """
        Processes a video.

        video_data (list): Information of the video to be
            processed.

        Example:

            [
                # Domain URL where te video came from
                "whatsapp.aucarvideo.com",
                # The ID of the video
                11,
                # The path to the video in the media folder
                "/media/contests/videos/Nelly_Furtado_-_Promiscuous_ft._Timbaland.avi",
                # The name of the converted version of the video.
                "/media/contests/videos/Nelly_Furtado_-_Promiscuous_ft._Timbaland_Converted.mp4"
            ]
    """
    
    domain_url, video_id, input_file, output_file = video_data
    

    code, out, err = process_video(input_file,output_file)
    success = 0
    if code == success:
        logging.info(f'Process success {input_file}')
        notify_client(domain_url,video_id)
        return code
       
    logging.error(f'{out} {err} {input_file}')
    return code


def process_videos():
    """
        Processes the videos
    """

    videos_to_process = get_videos_to_be_processed()

    if not videos_to_process:
        logging.info(f'Not videos to process')


    # Pass every video data in 'videos_to_be_processed' 
    # to the process_client_video function.
    for video_info in videos_to_process:
        process_client_video(video_info)

def process_videos_multithreading():

    """
        Processes the videos in parallel
    """

    videos_to_process = get_videos_to_be_processed()
    if not videos_to_process:
        logging.info(f'Not videos to process')
        return

    processes = int(max(multiprocessing.cpu_count() / 2,1))
    logging.info(f'Starting multitreaing processing with {processes} processes')
    

    # start 4 worker processes
    with multiprocessing.Pool(processes=processes) as pool:
        pool.map(process_client_video, videos_to_process)
        # pool.join()

    logging.info(f'Ending multitreaing processing with {processes} processes')


def notify_client(domain_url,video_id):
    """
        Notify to a client that a video has been processed
        succesfully.

        domain_url (str): is the client home url without path,
            example: facebook.aucarvideo.com.

        video_id (int): The id of the video being processed.
    """

    response = requests.post(
        url=CLIENT_VIDEO_STATUS_URL, 
        headers={'host':domain_url},
        data= {'video_id':video_id}
    )

    if response.status_code == 200:
        logging.info(f'Notification sended to {domain_url} about video {video_id}')
    else:
        logging.error(f'Notification error to {domain_url} about videos {video_id}')


if __name__ == '__main__':
    # process_videos()
    process_videos_multithreading()