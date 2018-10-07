#!/bin/bash

# IP Address of the web server (or load balancer)
export WEB_IP=""
# Port on which the web server (or load balancer) is running
export WEB_PORT=""
# Filename of the file on which logs will be written
export WEB_LOG_FILE_PATH="/usr/src/app/worker.log"
# Endpoint url of the web API to notify the status of the video convertion
export VIDEO_NOTIF_ENPOINT_URL="http://${WEB_IP}:${WEB_PORT}/api/contest/videos/status/"

# The folder on which the media folder will be created.
# On this folder the NFS remote folder will be mounted.
export MEDIA_PATH=/home/app/

# Broker IP
export BROKER_IP=""
# Borker Port
export BROKER_PORT=""
# Broker virtualhost
export BROKER_VHOST="aucarvideo"
# Broker username
export BROKER_USER="aucarvideo"
# Broker passwd
export BROKER_PASS="aucarvideo"

export CELERY_BROKER_URL="amqp://${BROKER_PASS}:aucar@${BROKER_IP}:${BROKER_PORT}/${BROKER_VHOST}"

echo "Running Celery Worker.."

celery -A /home/app/tasks worker --loglevel=info --concurrency=1
