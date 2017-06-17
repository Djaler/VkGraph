from celery import Celery
from flask_caching import Cache

import config

cache = Cache(config={'CACHE_TYPE': 'simple'})
celery = Celery(__name__, broker=config.CELERY_BROKER_URL)
