from app import celery
from app.factory import create_app

create_app(celery)
