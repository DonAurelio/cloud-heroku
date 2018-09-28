#!/bin/bash

# Setting env variables required to send emails
# and other settings required for the application 
# to work correctly
source secrets.sh

./manage.py makemigrations --noinput

./manage.py migrate_schemas --noinput

./manage.py migrate_schemas --shared --noinput

# colecting staticfiles in sstatic dir
./manage.py collectstatic --noinput

# Creating the public domain to acces the application
./manage.py create_public_tenant

# Running the django application
gunicorn aucarvideo.wsgi --timeout 600 -b 0.0.0.0:80
