#!/bin/bash

# Setting env variables required to send emails
# and other settings required for the application 
# to work correctly
source secrets.sh

./manage.py makemigrations --noinput

./manage.py migrate --noinput

# colecting staticfiles in static dir
./manage.py collectstatic --noinput

# Running the django application
gunicorn aucarvideo.wsgi --timeout 600 -b 0.0.0.0:80
