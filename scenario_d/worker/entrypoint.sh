#!/bin/bash

echo "Removing log files .."
rm -rf /home/app/logs/celery.*

echo "Running Supervisor .."
# Start Supervisor
supervisord -c /etc/supervisor/supervisord.conf

# echo "Running flower monitor at port 5555"
cd /home/app/celery/
celery -A tasks flower --broker=${BROKER_URL}

# celery -A tasks worker --loglevel=info --concurrency=1
