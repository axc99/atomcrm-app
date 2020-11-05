import glob
import os
import logging
import dukpy
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from flask_script import Manager

from flaskr import app, init_db

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

manager = Manager(app)


@manager.command
def runserver():
    extra_files = None

    if os.environ.get('FLASK_ENV') == 'production':
        compile()
    else:
        extra_files = glob.glob('flaskr/**/*.js', recursive=True)

    init_db()

    handler = RotatingFileHandler('logs/errors.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)

    app.run(host='0.0.0.0',
            port=4000,
            extra_files=extra_files)


@manager.command
def compile():
    dir = os.path.dirname(__file__)

    # Get all .js methods in views
    filenames = glob.glob('flaskr/**/*.js', recursive=True)
    filenames = [f for f in filenames if not f.endswith('.prod.js')]

    for filename in filenames:
        # Get JavaScript code from file
        file = open(os.path.join(dir, filename), 'r')
        code = file.read()
        file.close()

        # Compile ES6/ES7 to ES5 with BabelJS
        # More information: https://babeljs.io/docs/en/
        compiled_code = dukpy.babel_compile(code, presets=['stage-2'])['code']

        # Save compiled JavaScript code to production file
        prod_filename = "{}.{}".format(os.path.splitext(filename)[0], 'prod.js')
        prod_file = open(prod_filename, "w")
        prod_file.write(compiled_code)
        prod_file.close()

        print('Compiled: {}'.format(prod_filename))


if __name__ == "__main__":
    manager.run()
