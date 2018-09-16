#!/bin/bash

# Reference: https://bencane.com/2015/09/22/preventing-duplicate-cron-job-executions/

PIDFILE=/usr/src/app/script.pid
if [ -f $PIDFILE ]
then
  PID=$(cat $PIDFILE)
  ps -p $PID > /dev/null 2>&1
  if [ $? -eq 0 ]
  then
    echo "Process already running"
    exit 1
  else
    ## Process not found assume not running
    echo $$ > $PIDFILE
    if [ $? -ne 0 ]
    then
      echo "Could not create PID file"
      exit 1
    fi
  fi
else
  echo $$ > $PIDFILE
  if [ $? -ne 0 ]
  then
    echo "Could not create PID file"
    exit 1
  fi
fi
echo "Running cron......"
/usr/local/bin/python3.6 /usr/src/app/script.py /usr/src/app/ nginx 80 /usr/src/app/time.log

rm $PIDFILE