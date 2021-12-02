import os
from uuid import uuid4

TEMPLATES_AUTO_RELOAD = True
CSRF_ENABLED = True
SECRET_KEY = str(uuid4())
CELERY_BROKER_URL = os.environ.get('REDISCLOUD_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
BROKER_TRANSPORT_OPTIONS = {
    'max_connections': 20,
}
