web: newrelic-admin run-program gunicorn aucarvideo.wsgi
worker: celery -A tasks.app worker -l INFO

