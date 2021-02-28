import json
import os

import werkzeug
from flask import request, jsonify
from flask_babel import _
from werkzeug.exceptions import HTTPException

from flaskr import db
from flaskr import app
from flaskr.views import views_map
from flaskr.requests import requests_map
import flaskr.api as api_methods
from flaskr.models.lead import Lead
from flaskr.models.status import Status
from flaskr.models.field import Field
from flaskr.models.tag import Tag
from flaskr.models.task import Task
from flaskr.models.token import Token
from flaskr.models.installation_card_settings import InstallationCardSettings
from flaskr.models.installation_extension_settings import InstallationExtensionSettings
from flaskr.secure import validate_api_token, validate_secret_key
from flaskr.extensions import get_extension_by_id, extensions_map


@app.route('/')
def index():
    return '<a href="{}">Atom CRM</a>'.format(os.environ.get('APP_PAGE_URL'))


# Requests
@app.route('/req', methods=['POST'])
def req():
    data = request.get_json()
    is_secret_key_valid = validate_secret_key(data['appSecretKey'])
    req = data['req']
    params = data['params']
    request_data = {
        'installation_id': data['installationId'],
        'workspace_id': data['workspaceId'],
        'user_id': data['userId'],
        'app_id': data['appId'],
        'lang_key': data['langKey'],
        'timezone_offset': data.get('timezoneOffset', 0)
    }

    # Check secret key
    if not is_secret_key_valid:
        return {
                   'message': 'Wrong request data'
               }, 401

    # Get view
    if req == 'getView':
        view_key = params['key']
        view_params = params.get('params', {})

        if not views_map.get(view_key):
            return {
                'res': 'err',
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

            view.before_get_data(view_params, request_data)
            result_view['data'] = view.get_data(view_params, request_data)

            view.before_get_methods(view_params, request_data)
            result_view['methods'] = view.get_methods(view_params, request_data)

            view.before_get_scheme(view_params, request_data)
            result_view['scheme'] = view.get_scheme(view_params, request_data)

            result_view['script'] = view.script

            return {
                'res': 'ok',
                **result_view
            }

    # Other requests
    else:
        if not requests_map.get(req):
            raise Exception()
        else:
            request_func = requests_map[req]
            request_result = request_func(params, request_data)

            return request_result


# API
@app.route('/api/v<version>/<resource>', methods=['GET', 'POST', 'PATCH'])
@app.route('/api/v<version>/<resource>/<resource_id>', methods=['GET', 'POST', 'PATCH'])
def api_method(resource, resource_id=None, token=None, version=1):
    if not token:
        token = request.headers.get('Authorization')

    if int(version) not in (1,):
        return {
           'message': 'API version not supported'
        }, 401

    is_token_valid, nepkit_installation_id = validate_api_token(token)

    if not is_token_valid:
        return {
           'message': 'Invalid token'
        }, 401

    data = {}
    if request.is_json:
        data = request.get_json()

    method = None
    if resource == 'leads':
        if request.method == 'GET' and resource_id:
            method = 'get_leads'
        elif request.method == 'POST':
            method = 'create_lead'
        elif request.method == 'PATCH' and resource_id:
            method = 'update_lead'

    if not method:
        return 'Wrong request', 400
    else:
        method_func = getattr(api_methods, method)

        return method_func(resource_id, data, nepkit_installation_id)


# Extension web hook
@app.route('/ext/<extension_key>/wh/<webhook_token>', methods=['POST'])
@app.route('/ext/<extension_key>/wh/<webhook_token>/<webhook_key>', methods=['POST'])
def extension_webhook(extension_key, webhook_token, webhook_key=None):
    extension_class = extensions_map[extension_key]

    installation_extension_id, installation_extension_token = webhook_token.split('_')
    installation_extension_settings = InstallationExtensionSettings.query \
        .filter_by(id=installation_extension_id,
                   token=installation_extension_token) \
        .first()

    if not installation_extension_settings or not extension_class:
        return {
                   'message': 'Wrong request data'
               }, 401

    return extension_class.catch_webhook(installation_extension_settings, webhook_key)
