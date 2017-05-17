#!/bin/bash

for TOKEN in $TOKENS
do
    export ACCESS_TOKEN=$TOKEN
    celery worker -A app.celery -c 1 &
done

gunicorn -b "0.0.0.0:$PORT" app:app