from dotenv import find_dotenv, load_dotenv

from app import app

if __name__ == '__main__':
    load_dotenv(find_dotenv())

    app.run(debug=True)
