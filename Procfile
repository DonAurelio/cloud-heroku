web: gunicorn aucarvideo.wsgi --log-file -
worker: celery -A tasks.app worker -l INFO

