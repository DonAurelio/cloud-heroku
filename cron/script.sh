#!/bin/bash

MEDIA_DIR=/usr/src/app/
SERVICE=web
SERVICE_PORT=80

# Running the django application
echo "Running video processing cron"
/usr/local/bin/python /usr/src/app/main.py ${MEDIA_DIR} ${SERVICE} ${SERVICE_PORT} 
echo "Ending video processing cron"