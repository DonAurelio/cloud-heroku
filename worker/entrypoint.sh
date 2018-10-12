#!/bin/bash

echo "Running Celery Worker.."

celery -A tasks worker --loglevel=info --concurrency=1
