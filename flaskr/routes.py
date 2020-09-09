import os
from flask import request
from flaskr import app
from flaskr.views import views_map
from flaskr.requests import requests_map
import flaskr.api as api_methods
from flaskr.secure import validate_api_token, validate_secret_key


# Index page
@app.route('/')
def index():
    return '<a href="{}">Atom CRM</a>'.format(os.environ.get('APP_PAGE_URL'))


# Requests
@app.route('/req', methods=['POST'])
def req():
    data = request.get_json()
    is_secret_key_valid = validate_secret_key(data['appSecretKey'])
    request_data = {
        'installation_id': data['installationId'],
        'system_id': data['systemId'],
        'user_id': data['userId'],
        'app_id': data['appId'],
        'lang_key': data['langKey']
    }

    # Check secret key
    if not is_secret_key_valid:
        return {
            'message': 'Wrong request data'
        }, 401

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

            view.before(view_params, request_data)

            view.before_get_meta(view_params, request_data)
            result_view['meta'] = view.get_meta(view_params, request_data)

            view.before_get_header(view_params, request_data)
            result_view['header'] = view.get_header(view_params, request_data)

            view.before_get_methods(view_params, request_data)
            result_view['methods'] = view.get_methods(view_params, request_data)

            view.before_get_schema(view_params, request_data)
            result_view['schema'] = view.get_schema(view_params, request_data)

            return {
                '_res': 'ok',
                **result_view
            }

    # Other requests
    else:
        request_name = data['_req']
        request_params = data

        if not requests_map.get(request_name):
            raise Exception()
        else:
            request_func = requests_map[request_name]
            request_result = request_func(request_params, request_data)

            return request_result


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
    is_token_valid, veokit_installation_id = validate_api_token(token)

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

        return method_func(data, veokit_installation_id)
