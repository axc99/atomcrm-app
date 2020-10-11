import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_babel import Babel


app = Flask(__name__)

app.debug = os.environ.get('FLASK_ENV') == 'production'
app.secret_key = os.environ.get('APP_SECRET_KEY')

babel = Babel(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://{}:{}@db/{}'.format(os.environ.get('POSTGRES_USER'),
                                                                        os.environ.get('POSTGRES_PASSWORD'),
                                                                        os.environ.get('POSTGRES_DB'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


# DB and migrations
db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.create_all()


@babel.localeselector
def get_locale():
    data = request.get_json()
    lang_key = data['langKey'] if data else None
    langs = ('en', 'ru')

    if not lang_key or lang_key not in langs:
        lang_key = 'en'

    return lang_key


# Routing
import flaskr.routes
