from celery import Celery
from flask import Flask
from flask_caching import Cache

app = Flask(__name__)
app.config.from_object('config')

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

from .controllers import api, views
