import os
from dotenv import load_dotenv
from flaskr import app

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
