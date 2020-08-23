import os
from dotenv import load_dotenv
from flaskr import app, routes

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
