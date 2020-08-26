import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

app.debug = os.environ.get('FLASK_ENV') == 'production'
app.secret_key = os.environ.get('SECRET_KEY')

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://{}:{}@db/{}'.format(os.environ.get('POSTGRES_USER'),
                                                                        os.environ.get('POSTGRES_PASSWORD'),
                                                                        os.environ.get('POSTGRES_DB'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


# DB and migrations
db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.create_all()


# Routing
import flaskr.routes
