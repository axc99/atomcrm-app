import os
from flask import Flask

production_mode = os.environ.get('FLASK_ENV') == 'production'

app = Flask(__name__)
app.debug = not production_mode
