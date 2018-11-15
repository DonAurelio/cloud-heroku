web: newrelic-admin run-program gunicorn aucarvideo.wsgi
worker: NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program celery -A tasks.app worker -l INFO

