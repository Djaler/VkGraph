from flask import Flask
from flask_caching import Cache

app = Flask(__name__)
app.config.from_object('config')
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

from .controllers import api, views
