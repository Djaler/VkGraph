from flask import Flask

from app.controllers.api import api
from app.controllers.views import views


def create_app(celery, cache=None):
    app = Flask(__name__)
    app.config.from_object('config')
    
    if cache:
        cache.init_app(app)
    celery.conf.update(app.config)
    
    app.register_blueprint(views)
    app.register_blueprint(api)
    
    return app
