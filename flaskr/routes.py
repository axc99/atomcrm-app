import os
from flask import request
from flask_babel import _
from flaskr import db
from flaskr import app
from flaskr.views import views_map
from flaskr.requests import requests_map
import flaskr.api as api_methods
from flaskr.models.lead import Lead
from flaskr.models.status import Status
from flaskr.models.field import Field
from flaskr.models.tag import Tag
from flaskr.models.token import Token
from flaskr.models.installation_card_settings import InstallationCardSettings
from flaskr.models.installation_extension_settings import InstallationExtensionSettings
from flaskr.secure import validate_api_token, validate_secret_key
from flaskr.views.extensions.extensions import get_extension_by_id, extensions_map


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
        'system_id': data['systemId'],
        'user_id': data['userId'],
        'app_id': data['appId'],
        'lang_key': data['langKey'],
        'timezone_offset': data['timezoneOffset']
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

            view.before_get_methods(view_params, request_data)
            result_view['methods'] = view.get_methods(view_params, request_data)

            view.before_get_schema(view_params, request_data)
            result_view['schema'] = view.get_schema(view_params, request_data)

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


# Web hook
@app.route('/wh', methods=['POST'])
def webhook():
    data = request.get_json()
    is_secret_key_valid = validate_secret_key(data['appSecretKey'])

    event = data['event']
    lang_key = data.get('langKey')

    # Check secret key
    if not is_secret_key_valid:
        return {
           'message': 'Wrong request data'
        }, 401

    if event == 'installApp':
        # Add statuses
        default_statuses = [
            {'index': 0, 'color': 'blue', 'name': _('r_webhook_defaultStatuses_lead')},
            {'index': 1, 'color': 'blue', 'name': _('r_webhook_defaultStatuses_contacted')},
            {'index': 2, 'color': 'pink', 'name': _('r_webhook_defaultStatuses_qualified')},
            {'index': 3, 'color': 'green', 'name': _('r_webhook_defaultStatuses_proposalMade')},
            {'index': 4, 'color': 'green', 'name': _('r_webhook_defaultStatuses_win')},
            {'index': 5, 'color': 'red', 'name': _('r_webhook_defaultStatuses_lost')}
        ]
        for default_status in default_statuses:
            new_status = Status()
            new_status.index = default_status['index']
            new_status.color = default_status['color']
            new_status.name = default_status['name']
            new_status.veokit_installation_id = data['installationId']

            db.session.add(new_status)

        # Add fields
        default_fields = [
            {'index': 0, 'name': _('r_webhook_defaultStatuses_firstName'), 'value_type': 'string', 'max': 40, 'as_title': True, 'primary': False},
            {'index': 0, 'name': _('r_webhook_defaultStatuses_lastName'), 'value_type': 'string', 'max': 60, 'as_title': True, 'primary': False},
            {'index': 0, 'name': _('r_webhook_defaultStatuses_email'), 'value_type': 'string', 'max': 260, 'as_title': False, 'primary': True},
            {'index': 0, 'name': _('r_webhook_defaultStatuses_mobilePhone'), 'value_type': 'string', 'max': 30, 'as_title': False, 'primary': True}
        ]
        for default_field in default_fields:
            new_field = Field()
            new_field.index = default_field['index']
            new_field.name = default_field['name']
            new_field.value_type = default_field['value_type']
            new_field.max = default_field['max']
            new_field.as_title = default_field['as_title']
            new_field.primary = default_field['primary']
            new_field.veokit_installation_id = data['installationId']

            db.session.add(new_field)

        # Create card settings
        new_card_settings = InstallationCardSettings()
        new_card_settings.amount_enabled = False
        new_card_settings.currency = 'usd'
        new_card_settings.veokit_installation_id = data['installationId']
        db.session.add(new_card_settings)
        db.session.commit()

    elif event == 'uninstallApp':
        # Delete all data
        InstallationCardSettings.query.filter_by(veokit_installation_id=data['installationId']).delete()
        Lead.query.filter_by(veokit_installation_id=data['installationId']).delete()
        Status.query.filter_by(veokit_installation_id=data['installationId']).delete()
        Field.query.filter_by(veokit_installation_id=data['installationId']).delete()
        Tag.query.filter_by(veokit_installation_id=data['installationId']).delete()
        Token.query.filter_by(veokit_installation_id=data['installationId']).delete()

        db.session.commit()

    elif event == 'enableExtension':
        extension_class = get_extension_by_id(data['extensionId'])

        # Enable extension
        new_extension_settings = InstallationExtensionSettings()
        new_extension_settings.token = InstallationExtensionSettings.generate_token()
        new_extension_settings.veokit_installation_id = data['installationId']
        new_extension_settings.veokit_extension_id = data['extensionId']
        new_extension_settings.data = extension_class.get_default_data()
        db.session.add(new_extension_settings)
        db.session.commit()

    elif event == 'disableExtension':
        extension_class = get_extension_by_id(data['extensionId'])

        # Disable extension
        InstallationExtensionSettings.query\
            .filter_by(veokit_installation_id=data['installationId'],
                       veokit_extension_id=data['extensionId'])\
            .delete()
        db.session.commit()

    return {}


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


# Extension web hook
@app.route('/ext/<extension_key>/wh/<webhook_token>', methods=['POST'])
@app.route('/ext/<extension_key>/wh/<webhook_token>/<webhook_key>', methods=['POST'])
def extension_webhook(extension_key, webhook_token, webhook_key=None):
    extension_class = extensions_map[extension_key]

    installation_extension_id, installation_extension_token = webhook_token.split('_')
    installation_extension_settings = InstallationExtensionSettings.query\
                                .filter_by(id=installation_extension_id,
                                           token=installation_extension_token)\
                                .first()

    if not installation_extension_settings or not extension_class:
        return {
           'message': 'Wrong request data'
        }, 401

    return extension_class.catch_webhook(installation_extension_settings, webhook_key)
