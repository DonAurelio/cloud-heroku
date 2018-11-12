web: newrelic-admin run-program python3.6 manage.py run_gunicorn -b "0.0.0.0:$PORT" -w 3
worker: celery -A tasks.app worker -l INFO

