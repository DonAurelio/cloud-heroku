#!/usr/local/bin/python3.6
# -*- coding: utf-8 -*-

import requests
import datetime
import logging
import sys
import subprocess
import os
import time


logging.basicConfig(
    format='%(levelname)s : %(asctime)s : %(message)s',
    level=logging.DEBUG
)

# To print loggin information in the console
logging.getLogger().addHandler(logging.StreamHandler())


def take_time(func):
    def wrapper(*args):
        start = time.time()
        values = func(*args)
        end = time.time()
        file_size = os.path.getsize(file_path)
        text = f'{end-start}\t{file_size}\t{input_file}\t{output_file}\n'

        with open('time.log','w+') as file:
            print(f'video processing time {end-start}')
            file.write(text)

        return values

    return wrapper


class VidesProcessor(object):

    WEB_PUBLIC_URL = 'aucarvideo.com'

    def __init__(self,media_path,hostname='localhost',port='8000'):
        
        logging.info(f'Procesing path "{media_path}"')

        self.media_path = media_path
        self.hostname = hostname
        self.port = port

        self.succes_videos_id = []
        self.error_videos_id = []

    def server_url(self,path=''):
        return f'http://{self.hostname}:{self.port}{path}'

    def _request_tenants_urls(self):
        url = self.server_url(path='/api/client/list')
        response = requests.get(
            url=url, 
            headers={'host':self.WEB_PUBLIC_URL}
        )

        return response.json() if response.status_code == 200 else []

    def _requests_tenant_videos(self,domain_url):
        url = self.server_url(path='/api/contest/videos/status/')
        response = requests.get(
            url=url, 
            headers={'host':domain_url}
        )

        return response.json() if response.status_code == 200 else []

    def _notify_tenant(self,domain_url,data):
        url = self.server_url(path='/api/contest/videos/status/')
        response = requests.post(
            url=url, 
            headers={'host':domain_url},
            data=data
        )

        return response.status_code


    def _request_tenants_videos(self):
        videos_by_domain = {}

        try:
            domain_urls = self._request_tenants_urls()
            for domain_url in domain_urls:
                videos_paths = self._requests_tenant_videos(domain_url)
                if videos_paths:
                    videos_by_domain[domain_url] = videos_paths

            return videos_by_domain
        except requests.exceptions.ConnectionError as e:
            logging.error(
                f'Connection can not be stablished {self.hostname} {self.port}'
            )


    def process_videos(self):

        videos_by_domain = self._request_tenants_videos()

        if videos_by_domain:
            success_code = 0
            for  domain_url, video_info in videos_by_domain.items():

                for video_id, input_file, output_file in video_info:

                    #  Take time of video processing step
                    start = time.time()
                    code, out, err  = self._process_video(input_file,output_file)
                    end = time.time()

                    #  Save the time in miliseconds, the video processing
                    #  status code, input and output files path.
                    file_size = os.path.getsize(input_file)
                    with open('time.log','w+') as file:
                        text = f'{end-start}\t{code}\t{file_size}\t{input_file}\t{output_file}\n'
                        logging.info(text)
                        file.write(text)

                    if code == success_code:
                        
                        # Video processing was converted correctly
                        logging.info(f'Process success {input_file}')
                        self._notify_web_app(domain_url,video_id)
                        # WE HAVE TO NOTIFY WEB APP WHEN A VIDEO FAILS 
                        # IN PROCESSING

                    else:
                        # An erro has ocurred during videos processing
                        logging.error(f'{out} {err} {input_file}')
                        
       
        else:
            logging.info('No videos for processing')

    @take_time
    def _process_video(self,input_file,output_file):
        # Remove the first '/' on the video path
        input_file = input_file[1:]
        output_file = output_file[1:]

        input_file = os.path.join(self.media_path,input_file)
        output_file = os.path.join(self.media_path,output_file)

        exists = os.path.isfile(output_file)
        if exists:
            # If the files already exists.
            # it is not neccesarry to perform
            #  processign again
            return 0, None, None

        logging.info(f'Start processing {input_file} to {output_file}')

        command = f'ffmpeg -i {input_file} {output_file}'
        
        process = subprocess.run(
            args=command,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            shell=True, 
            universal_newlines=True,
        )

        return process.returncode, process.stdout, process.stderr

    def _notify_web_app(self,domain_url,video_id):
        
        data = {'video_id':video_id}
        status = self._notify_tenant(domain_url,data)

        if status == 200:
            logging.info(f'Notification success to {domain_url} about video {video_id}')
        else:
            logging.error(f'Notification error to {domain_url} regarding videos {video_id}')


if __name__ == '__main__':

    media_path = sys.argv[1] if len(sys.argv) > 1 else ''
    hostname = sys.argv[2] if len(sys.argv) > 2 else 'localhost'
    port = sys.argv[3] if len(sys.argv) > 3 else '8000'

    processor = VidesProcessor(media_path,hostname,port)
    processor.process_videos()
