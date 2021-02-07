from cerberus import Validator

from flaskr import db
from flask_babel import _

from flaskr.extensions import get_extension_by_id
from flaskr.models.field import Field
from flaskr.models.installation_card_settings import InstallationCardSettings
from flaskr.models.lead import Lead
from flaskr.models.status import Status
from flaskr.models.installation_extension_settings import InstallationExtensionSettings


# Install app
from flaskr.models.tag import Tag
from flaskr.models.task import Task
from flaskr.models.token import Token


def handle_install_app(params, request_data):
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
        new_status.nepkit_installation_id = request_data['installation_id']

        db.session.add(new_status)

    # Add fields
    default_fields = [
        {'index': 0, 'name': _('r_webhook_defaultStatuses_firstName'), 'value_type': 'string', 'max': 40,
         'board_visibility': 'title', 'primary': False},
        {'index': 1, 'name': _('r_webhook_defaultStatuses_lastName'), 'value_type': 'string', 'max': 60,
         'board_visibility': 'title', 'primary': False},
        {'index': 2, 'name': _('r_webhook_defaultStatuses_email'), 'value_type': 'email', 'max': 260,
         'board_visibility': 'subtitle', 'primary': True},
        {'index': 3, 'name': _('r_webhook_defaultStatuses_mobilePhone'), 'value_type': 'phone', 'max': 30,
         'board_visibility': 'subtitle', 'primary': True}
    ]
    for default_field in default_fields:
        new_field = Field()
        new_field.index = default_field['index']
        new_field.name = default_field['name']
        new_field.value_type = default_field['value_type']
        new_field.max = default_field['max']
        new_field.board_visibility = default_field['board_visibility']
        new_field.primary = default_field['primary']
        new_field.nepkit_installation_id = request_data['installation_id']

        db.session.add(new_field)

    # Add tasks
    default_tasks = [
        {'index': 0, 'name': _('r_webhook_defaultTasks_sendLetter')},
        {'index': 1, 'name': _('r_webhook_defaultTasks_makeCall')}
    ]
    for default_task in default_tasks:
        new_task = Task()
        new_task.index = default_task['index']
        new_task.name = default_task['name']
        new_task.nepkit_installation_id = request_data['installation_id']

        db.session.add(new_task)

    # Get currency by lang
    currency_by_lang = {'en': 'usd',
                        'ru': 'rub'}
    currency = currency_by_lang[request_data['lang_key']] if request_data['lang_key'] in currency_by_lang else 'en'

    # Create card settings
    new_card_settings = InstallationCardSettings()
    new_card_settings.amount_enabled = False
    new_card_settings.currency = currency
    new_card_settings.nepkit_installation_id = request_data['installation_id']
    db.session.add(new_card_settings)
    db.session.commit()

    return {
        'res': 'ok'
    }


# Uninstall app
def handle_uninstall_app(params, request_data):
    # Delete all data
    InstallationCardSettings.query.filter_by(nepkit_installation_id=request_data['installation_id']).delete()
    Lead.query.filter_by(nepkit_installation_id=request_data['installation_id']).delete()
    Status.query.filter_by(nepkit_installation_id=request_data['installation_id']).delete()
    Field.query.filter_by(nepkit_installation_id=request_data['installation_id']).delete()
    Tag.query.filter_by(nepkit_installation_id=request_data['installation_id']).delete()
    Token.query.filter_by(nepkit_installation_id=request_data['installation_id']).delete()

    db.session.commit()

    return {
        'res': 'ok'
    }


# Enable extension
def handle_enable_extension(params, request_data):
    extension_class = get_extension_by_id(params['extensionId'])

    # Enable extension
    new_extension_settings = InstallationExtensionSettings()
    new_extension_settings.token = InstallationExtensionSettings.generate_token()
    new_extension_settings.nepkit_installation_id = request_data['installation_id']
    new_extension_settings.nepkit_extension_id = params['extensionId']
    new_extension_settings.data = extension_class.get_default_data()
    db.session.add(new_extension_settings)
    db.session.commit()

    return {
        'res': 'ok'
    }


# Disable extension
def handle_disable_extension(params, request_data):
    extension_class = get_extension_by_id(params['extensionId'])

    # Disable extension
    InstallationExtensionSettings.query \
        .filter_by(nepkit_installation_id=request_data['installation_id'],
                   nepkit_extension_id=params['extensionId']) \
        .delete()
    db.session.commit()

    return {
        'res': 'ok'
    }
