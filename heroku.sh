#!/bin/bash
celery worker -A app.celery -c 1 &
gunicorn -b "0.0.0.0:$PORT" app:app