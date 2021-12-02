#!/bin/bash

for TOKEN in $TOKENS
do
    export ACCESS_TOKEN=$TOKEN
    celery -A run_celery.celery worker -c 1 &
done

gunicorn -b "0.0.0.0:$PORT" run_app:app
