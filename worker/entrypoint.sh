#!/bin/bash

# IP Address of the web server (or load balancer)
export WEB_IP="localhost"
# Port on which the web server (or load balancer) is running
export WEB_PORT="8000"
# Filename of the file on which logs will be written
export WEB_LOG_FILE_PATH="/usr/src/app/worker.log"
# Endpoint url of the web API to notify the status of the video convertion
export VIDEO_NOTIF_ENPOINT_URL="http://${WEB_IP}:${WEB_PORT}/api/contest/videos/status/"

echo "Running Celery Worker.."

celery -A /home/app/tasks worker --loglevel=info --concurrency=1
