from app import cache, celery
from app.factory import create_app

app = create_app(celery, cache)

if __name__ == '__main__':
    app.run(debug=True)
