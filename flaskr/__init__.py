import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_babel import Babel


app = Flask(__name__)

if os.environ.get('FLASK_ENV') == 'production':
    app = Flask(__name__)
    app.debug = False
else:
    app = Flask(__name__, static_url_path='/static/', static_folder='./public/static')
    app.debug = True
app.secret_key = os.environ.get('APP_SECRET_KEY')


# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://{}:{}@db/{}'.format(os.environ.get('POSTGRES_USER'),
                                                                        os.environ.get('POSTGRES_PASSWORD'),
                                                                        os.environ.get('POSTGRES_DB'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


# DB and migrations
db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.create_all()


# Babel
babel = Babel(app)
@babel.localeselector
def get_locale():
    supported_langs = ('en', 'ru')

    data = request.get_json()
    lang_key = data.get('langKey') if data else None

    if not lang_key or lang_key not in supported_langs:
        return 'en'
    else:
        return lang_key


# Routing
import flaskr.routes
