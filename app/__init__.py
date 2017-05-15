from celery import Celery
from dotenv import find_dotenv, load_dotenv
from flask import Flask
from flask_caching import Cache

load_dotenv(find_dotenv())

app = Flask(__name__)
app.config.from_object('config')

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

from .controllers import api, views
