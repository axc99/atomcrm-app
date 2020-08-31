import os
from flask import request
from flaskr import app
from flaskr.views import views_map
from flaskr.requests import requests_map
import flaskr.api as api_methods
from flaskr.secure import validate_api_token


# Index page
@app.route('/')
def index():
    return '<a href="{}">Atom CRM</a>'.format(os.environ.get('APP_PAGE_URL'))


# Requests
@app.route('/req', methods=['POST'])
def req():
    if not request.is_json:
        return {}, 400

    data = request.get_json()

    # Get view
    if data['_req'] == 'getView':
        view_key = data['key']
        view_params = data.get('params', {})

        if not views_map.get(view_key):
            return {
                '_res': 'err',
                "key": "view_not_found"
            }
        else:
            # Create view object
            view = views_map[view_key]()
            result_view = {}

            view.before(view_params)

            view.before_get_meta(view_params)
            result_view['meta'] = view.get_meta(view_params)

            view.before_get_header(view_params)
            result_view['header'] = view.get_header(view_params)

            view.before_get_methods(view_params)
            result_view['methods'] = view.get_methods(view_params)

            view.before_get_schema(view_params)
            result_view['schema'] = view.get_schema(view_params)

            return {
                '_res': 'ok',
                **result_view
            }

    # Custom requests
    else:
        request_name = data['_req']
        request_params = data.get('params', {})

        if not requests_map.get(request_name):
            raise Exception()
        else:
            request_func = requests_map[request_name]
            request_result = request_func(request_params)

            return {
                '_res': 'ok',
                **(request_result if isinstance(request_result, dict) else {})
            }


# Web hook
@app.route('/wh', methods=['POST'])
def webhook():
    # if not request.is_json:
    #     return {}, 400
    #
    # data = request.get_json()

    return 'ok'


# API
@app.route('/api/<token>/<method>', methods=['POST'])
def api_method(token, method):
    is_token_valid, veokit_system_id = validate_api_token(token)

    if not is_token_valid:
        return {
            'message': 'Invalid token'
        }, 401

    data = {}
    if request.is_json:
        data = request.get_json()

    method_map = {
        'getLeads': 'get_leads',
        'createLead': 'create_lead',
        'updateLead': 'update_lead',
        'archiveLead': 'archive_lead',

        'getStatuses': 'get_statuses',

        'getFields': 'get_fields'
    }

    if not method_map.get(method):
        return {
           'message': 'Method /{} does not exist'.format(method)
       }, 400
    else:
        method_func = getattr(api_methods, method_map[method])

        return method_func(data, veokit_system_id)
