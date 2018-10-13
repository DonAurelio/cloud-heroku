#!/bin/bash

echo "Removing log files .."

rm -rf celery.* flower.*

echo "Running Supervisor .."

# Start Supervisor
supervisord -c /etc/supervisor/supervisord.conf

# To check the processes are running
# ps aux

/bin/bash