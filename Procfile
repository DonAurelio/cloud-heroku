web: gunicorn -b 0.0.0.0:$PORT web/aucarvideo.wsgi --log-file -
worker: celery worker --app=worker/tasks.app

