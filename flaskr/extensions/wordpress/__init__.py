import os
from flaskr import db
from flask import request
from flask_babel import _

from flaskr.models.lead import Lead, LeadAction, LeadActionType
from flaskr.models.status import Status
from flaskr.extensions.extension import Extension
from flaskr.views.view import compile_js, method_with_vars

settings_script = compile_js('settings_script')


# Wordpress extension
# https://wordpress.com/
class WordpressExtension(Extension):
    id = os.environ.get('WORDPRESS_INTEGRATION_ID')
    key = 'wordpress'
    with_settings = False

    def __init__(self):
        Extension.__init__(self)
        self.name = 'Wordpress'
        self.settings_data = {
            'strs': {}
        }
        self.settings_script = settings_script

    @staticmethod
    def get_default_data():
        return {
            'plugin': 'contactform7'
        }

    def get_scheme_for_information(self, installation_extension_settings, params, request_data):
        fields = db.session.execute("""
                            SELECT 
                                f.*
                            FROM 
                                public.field AS f
                            WHERE
                                f.nepkit_installation_id = :nepkit_installation_id
                            ORDER BY 
                                f.index""", {
            'nepkit_installation_id': request_data['installation_id']
        })

        # Create markdown field-key list
        field_keys_list = ''
        for field in fields:
            field_keys_list += '- `f{}` - {} \r'.format(field['id'], field['name'])

        return [
            {
                '_com': 'Information',
                'content': _('v_extension_wordpress_information_content',
                             webhook_url='https://atomcrm.nepkit.team/ext/wordpress/wh/{}_{}'.format(
                                 installation_extension_settings.id, installation_extension_settings.token),
                             STATIC_URL=os.environ.get('STATIC_URL'),
                             field_keys_list=field_keys_list)
            }
        ]

    @staticmethod
    def catch_webhook(installation_extension_settings, webhook_key=None):
        data = request.get_json(force=True)

        fields = []
        for field_key, field_value in data.items():
            print('field', field_key, field_value)
            # Detect field with key f + id
            if field_key[0] == 'f' and field_key[1:].isnumeric():
                field_id = field_key[1:]
                fields.append({
                    'field_id': field_id,
                    'value': field_value
                })

                print({
                    'field_id': field_id,
                    'value': field_value
                })

        # Get first status and status by settings
        status = None
        if installation_extension_settings.data.get('default_status') != 'first':
            status = Status.query \
                .with_entities(Status.id) \
                .filter_by(nepkit_installation_id=installation_extension_settings.nepkit_installation_id,
                           id=installation_extension_settings.data.get('default_status')) \
                .first()
        if installation_extension_settings.data.get('default_status') == 'first' or not status:
            status = Status.query \
                .with_entities(Status.id) \
                .filter_by(nepkit_installation_id=installation_extension_settings.nepkit_installation_id) \
                .order_by(Status.index.asc()) \
                .first()

        # Create lead
        lead = Lead()
        lead.uid = Lead.get_uid()
        lead.nepkit_installation_id = installation_extension_settings.nepkit_installation_id
        lead.status_id = status.id

        db.session.add(lead)
        db.session.commit()

        if len(fields) > 0:
            lead.set_fields(fields, new_lead=True)

        # Log action
        new_action = LeadAction()
        new_action.type = LeadActionType.create_lead
        new_action.lead_id = lead.id
        new_action.new_status_id = lead.status_id
        db.session.add(new_action)
        db.session.commit()

        return '#{}'.format(lead.uid)
