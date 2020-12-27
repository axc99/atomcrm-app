import os
from flaskr import db
from flask import request
from flask_babel import _

from flaskr.models.lead import Lead, LeadAction, LeadActionType
from flaskr.models.status import Status
from flaskr.extensions.extension import Extension
from flaskr.views.view import compile_js, method_with_vars

settings_script = compile_js('settings_script')


# Tilda extension
# https://tilda.cc/
class TildaExtension(Extension):
    id = os.environ.get('TILDA_INTEGRATION_ID')
    key = 'tilda'
    with_settings = True

    def __init__(self):
        Extension.__init__(self)
        self.name = 'Tilda'

    @staticmethod
    def get_default_data():
        return {
            'default_status': 'first'
        }

    def get_data_for_settings(self, installation_extension_settings, params, request_data):
        statuses_q = db.session.execute("""
                        SELECT
                            s.*,
                            (SELECT COUNT(*) FROM public.lead AS l WHERE l.status_id = s.id AND l.archived = false) AS lead_count
                        FROM
                            public.status AS s
                        WHERE
                            s.nepkit_installation_id = :nepkit_installation_id
                        ORDER BY
                            s.index""", {
            'nepkit_installation_id': request_data['installation_id']
        })
        statuses = []
        for status in statuses_q:
            statuses.append({
                'id': status.id,
                'color': status.color,
                'name': status.name
            })

        return {
            'statuses': statuses,
            'strs': {

            },
            'installationExtensionSettings': {
                'id': installation_extension_settings.id,
                'data': installation_extension_settings.data
            }
        }

    def get_script_for_settings(self, installation_extension_settings, params, request_data):
        return settings_script

    def get_schema_for_information(self, installation_extension_settings, params, request_data):
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
                'content': _('v_extension_tilda_information_content',
                             webhook_url='https://nepkit.team/atomcrm/ext/tilda/wh/{}_{}'.format(installation_extension_settings.id, installation_extension_settings.token),
                             STATIC_URL=os.environ.get('STATIC_URL'),
                             field_keys_list=field_keys_list)
            }
        ]

    def get_schema_for_settings(self, installation_extension_settings, params, request_data):
        statuses = db.session.execute("""
            SELECT 
                s.*,
                (SELECT COUNT(*) FROM public.lead AS l WHERE l.status_id = s.id AND l.archived = false) AS lead_count
            FROM 
                public.status AS s
            WHERE
                s.nepkit_installation_id = :nepkit_installation_id
            ORDER BY 
                s.index""", {
            'nepkit_installation_id': request_data['installation_id']
        })

        status_options = [
            {'value': 'first', 'label': _('v_extension_tilda_information_settings_status_alwaysFirst')}
        ]
        for status in statuses:
            status_options.append({
                'value': status.id,
                'color': status.color,
                'label': status.name
            })

        return [
            {
                '_com': 'Form',
                '_id': 'extensionSettingsForm',
                'onFinish': 'onFinishForm',
                'fields': [
                    {
                        '_com': 'Field.Select',
                        'key': 'default_status',
                        'label': _('v_extension_tilda_information_settings_status'),
                        'options': status_options,
                        'value': installation_extension_settings.data.get('default_status'),
                        'rules': [
                            {'required': True,
                             'message': _('v_extension_tilda_information_settings_primary_rules_required')}
                        ]
                    }
                ],
                'buttons': [
                    {
                        '_com': 'Button',
                        'type': 'primary',
                        'submitForm': True,
                        'icon': 'save',
                        'label': _('v_extension_tilda_information_settings_save')
                    }
                ]
            }
        ]

    @staticmethod
    def catch_webhook(installation_extension_settings, webhook_key=None):
        data = request.form

        fields = []
        utm_marks = {}
        for field_key, field_value in data.items():
            # Detect field with key f + id
            if field_key[0] == 'f' and field_key[1:].isnumeric():
                field_id = field_key[1:]
                fields.append({
                    'field_id': field_id,
                    'value': field_value
                })
            elif field_key[:4] == 'utm_':
                utm_marks[field_key] = field_value

        # Get first status and status by settings
        status = None
        if installation_extension_settings.data.get('default_status') != 'first':
            status = Status.query \
                .with_entities(Status.id) \
                .filter_by(nepkit_installation_id=installation_extension_settings.nepkit_installation_id,
                           id=installation_extension_settings.data.get('default_status')) \
                .first()
        if installation_extension_settings.data.get('default_status') == 'first' or not status:
            status = Status.query\
                .with_entities(Status.id)\
                .filter_by(nepkit_installation_id=installation_extension_settings.nepkit_installation_id)\
                .order_by(Status.index.asc())\
                .first()

        # Create lead
        lead = Lead()
        lead.uid = Lead.get_uid()
        lead.nepkit_installation_id = installation_extension_settings.nepkit_installation_id
        lead.status_id = status.id
        # UTM marks
        lead.utm_source = utm_marks.get('utm_source', None)
        lead.utm_medium = utm_marks.get('utm_medium', None)
        lead.utm_campaign = utm_marks.get('utm_campaign', None)
        lead.utm_term = utm_marks.get('utm_term', None)
        lead.utm_content = utm_marks.get('utm_content', None)

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
