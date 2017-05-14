from uuid import uuid4

CSRF_ENABLED = True
SECRET_KEY = uuid4()
CACHE_TIMEOUT = 5 * 60
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
