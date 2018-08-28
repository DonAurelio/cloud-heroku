import requests
import datetime
import logging
import sys
import subprocess
import os

logging.basicConfig(
    format='%(levelname)s : %(asctime)s : %(message)s',
    filename='processing.log',level=logging.DEBUG
)


def get_args():
    media_path = sys.argv[1] if len(sys.argv) > 0 else ''
    hostname = sys.argv[2] if len(sys.argv) > 1 else 'localhost'
    port = sys.argv[3] if len(sys.argv) > 2 else '8000'

    return media_path, hostname, port


def request_videos_for_processing(public_host_name,port):
    tenants_domain_url = []
    pending_videos_urls = []
    response = requests.get(f'http://{public_host_name}:{port}/api/client/list')

    if response.status_code == 200:
        tenants_domain_url = response.json()
        
        for domain_url in tenants_domain_url:
            response = requests.get(f'http://{domain_url}:{port}/api/contest/videos/status/')
            pending_videos_urls += response.json()

    return pending_videos_urls


def process_video(input_file,output_file):

    # Remove the first '/' on the video path
    input_file = input_file[1:]
    output_file = output_file[1:]
    
    media_path, hostname, port = get_args()
    
    input_file = os.path.join(media_path,input_file)
    output_file = os.path.join(media_path,output_file)

    logging.info(f'Start processing {input_file} to {output_file}')

    command = f'ffmpeg -i {input_file} {output_file}'
    
    process = subprocess.run(
        args=command,
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        shell=True, 
        universal_newlines=True,
        # check=True
    )

    success_code = 0
    if process.returncode != success_code:
        logging.error(f'{process.stderr} {input_file}')
    else:        
        logging.info(f'Process {input_file} success!')


if __name__ == '__main__':

    media_path, hostname, port = get_args()
    logging.info(f'Search path {media_path}')

    videos_path = request_videos_for_processing(hostname,port)

    if not videos_path:
        logging.info('No videos for processing')

    for input_file, output_file in videos_path:
        process_video(input_file,output_file)
        






