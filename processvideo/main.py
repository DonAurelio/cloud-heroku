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

class VidesProcessor(object):

    def __init__(self,media_path,hostname='localhost',port='8000'):
        
        logging.info(f'Procesing path {media_path}')
        
        self.media_path = media_path
        self.hostname = hostname
        self.port = port

        self.succes_videos_id = []
        self.error_videos_id = []

    @property
    def public_url(self):
        return f'http://{self.hostname}:{self.port}/api/client/list'

    def _get_tenant_url(self,domain_url,port):
        return f'http://{domain_url}:{port}/api/contest/videos/status/'

    def _request_tenants_urls(self):
        response = requests.get(self.public_url)
        return response.json()

    def _request_videos_urls(self):
        videos_urls = []
        tenants_urls = self._request_tenants_urls()
        for domain_url in tenants_urls:
            tenant_url = self._get_tenant_url(domain_url,self.port)
            response = requests.get(tenant_url)
            videos_urls += response.json()

        return videos_urls

    def process_videos(self):

        videos_paths = self._request_videos_urls()
        
        if not videos_paths:
            logging.info('No videos for processing')

        success_code = 0
        for video_id, input_file, output_file in videos_paths:
            return_code = self._process_video(input_file,output_file)

            if return_code != success_code:
                # An erro has ocurred during videos processing
                logging.error(f'{process.stderr} {input_file}')
                self.error_videos_id.append(video_id)

            else:
                # Video processing was complited correctly
                logging.info(f'Process success {input_file}')
                self.succes_videos_id.append(video_id)

        # After all videos were processed we have to notify 
        # to the webapp which videos where processed so 
        # it change them status to 'Converted' in the database
        self._notify_web_app()

    def _process_video(self,input_file,output_file):
        # Remove the first '/' on the video path
        input_file = input_file[1:]
        output_file = output_file[1:]
        
        input_file = os.path.join(self.media_path,input_file)
        output_file = os.path.join(self.media_path,output_file)

        logging.info(f'Start processing {input_file} to {output_file}')

        command = f'ffmpeg -i {input_file} {output_file}'
        
        process = subprocess.run(
            args=command,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            shell=True, 
            universal_newlines=True,
        )

        return process.returncode

    def _notify_web_app(self):
        pass


if __name__ == '__main__':

    media_path = sys.argv[1] if len(sys.argv) > 0 else ''
    hostname = sys.argv[2] if len(sys.argv) > 1 else 'localhost'
    port = sys.argv[3] if len(sys.argv) > 2 else '8000'

    processor = VidesProcessor(media_path,hostname,port)
    processor.process_videos()




