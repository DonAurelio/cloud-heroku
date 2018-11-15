web: newrelic-admin run-program gunicorn --workers=3 aucarvideo.wsgi
worker: NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program celery -A tasks.app worker -l INFO

