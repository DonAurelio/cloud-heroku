#!/bin/sh

# Activating bash shell
bash

# Setting env variables required to send emails
# If this variables are not set the application
# may fail
source secrets.sh

# ./manage.py makemigrations customers --noinput --merge

./manage.py makemigrations --noinput --merge

./manage.py migrate_schemas --noinput

./manage.py migrate_schemas --shared --noinput

# colecting staticfiles in sstatic dir
./manage.py collectstatic --noinput

# Creating the public domain to acces the application
./manage.py create_public_tenant

# Running the django application
gunicorn aucarvideo.wsgi --timeout 600 -b 0.0.0.0:80
