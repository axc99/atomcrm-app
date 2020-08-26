import os
from flask import request
from flaskr import app, requests
from flaskr.views import views_map


# Index page
@app.route('/')
def index():
    return '<a href="{}">Atom CRM</a>'.format(os.environ.get('APP_PAGE_URL'))


# Requests
@app.route('/api', methods=['POST'])
def api():
    if not request.is_json:
        return {}, 400

    data = request.get_json()

    # Get view
    if data['_req'] == 'getView':
        view_key = data['key']

        #7
        if not views_map.get(view_key):
            return {
                '_res': 'err',
                "key": "view_not_found"
            }
        else:
            view = views_map[view_key]()

            return {
                'meta': view.meta,
                'methods': view.get_methods(),
                'header': view.get_header(),
                'schema': view.get_schema()
            }

    # Custom requests
    else:
        if not hasattr(requests, data['_req']):
            request_func = requests[data['_req']]

            return request_func()

    return {}


# Web hook
@app.route('/wh', methods=['POST'])
def webhook():
    if not request.is_json:
        return False, 400

    data = request.json()

    return True
