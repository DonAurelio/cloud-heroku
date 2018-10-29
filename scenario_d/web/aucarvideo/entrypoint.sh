#!/bin/bash

./manage.py makemigrations --noinput

./manage.py migrate --noinput

./manage.py collectstatic --noinput

gunicorn aucarvideo.wsgi --timeout 600 -b 0.0.0.0:80

# ./manage.py runserver 0.0.0.0:80

# /bin/bash