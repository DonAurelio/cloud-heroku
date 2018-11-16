web: newrelic-admin run-program gunicorn --workers=2 aucarvideo.wsgi
worker: NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program celery -A tasks.app worker --concurrency 4 -l INFO

