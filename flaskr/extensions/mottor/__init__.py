import os
from flaskr import db
from flask import request
from flask_babel import _
import urllib.parse as urlparse
from urllib.parse import parse_qs

from flaskr.models.installation_settings import InstallationSettings
from flaskr.models.lead import Lead, LeadAction, LeadActionType
from flaskr.models.status import Status
from flaskr.extensions.extension import Extension
from flaskr.views.view import compile_js, get_method, method_with_vars

settings_script = compile_js('settings_script')


# Mottor extension (LPgenerator, LPmotor)
# https://lpmotor.ru/
class MottorExtension(Extension):
    id = os.environ.get('MOTTOR_INTEGRATION_ID')
    key = 'mottor'
    with_settings = True

    def __init__(self):
        Extension.__init__(self)
        self.name = 'Mottor (LPgenerator)'

    @staticmethod
    def get_default_data():
        return {
            'defaultStatus': 'first'
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
                'form_defaultStatus': _('e_mottor_settings_form_defaultStatus'),
                'form_defaultStatus_alwaysFirst': _('e_mottor_settings_form_defaultStatus_alwaysFirst'),
                'form_defaultStatus_required': _('e_mottor_settings_form_defaultStatus_required'),
                'form_save': _('e_mottor_settings_form_save'),
                'notification_changesSaved': _('e_mottor_settings_notification_changesSaved')
            },
            'installationExtensionSettings': {
                'id': installation_extension_settings.id,
                'data': installation_extension_settings.data
            }
        }

    def get_script_for_settings(self, installation_extension_settings, params, request_data):
        return settings_script

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
                'content': _('v_extension_mottor_information_content',
                             webhook_url='https://atomcrm.nepkit.team/ext/mottor/wh/{}_{}'.format(installation_extension_settings.id, installation_extension_settings.token),
                             STATIC_URL=os.environ.get('STATIC_URL'),
                             field_keys_list=field_keys_list)
            }
        ]

    def get_scheme_for_settings(self, installation_extension_settings, params, request_data):
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
            {'value': 'first', 'label': _('v_extension_mottor_information_settings_status_alwaysFirst')}
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
                        'key': 'defaulttatus',
                        'label': _('v_extension_mottor_information_settings_status'),
                        'options': status_options,
                        'value': installation_extension_settings.data.get('defaultStatus'),
                        'rules': [
                            {'required': True,
                             'message': _('v_extension_mottor_information_settings_primary_rules_required')}
                        ]
                    }
                ],
                'buttons': [
                    {
                        '_com': 'Button',
                        'type': 'primary',
                        'submitForm': True,
                        'icon': 'save',
                        'label': _('v_extension_mottor_information_settings_save')
                    }
                ]
            }
        ]

    # def get_methods_for_settings(self, installation_extension_settings, params, request_data):
    #     methods = compiled_methods.copy()
    #
    #     methods['onFinishForm'] = method_with_vars(methods['onFinishForm'], {'INSTALLATION_EXTENSION_SETTINGS_ID': installation_extension_settings.id})
    #
    #     return methods

    @staticmethod
    def catch_webhook(installation_extension_settings, webhook_key=None):
        data = request.form
        referer = request.headers.get('Referer')

        utm_marks = {}
        if referer:
            search_params = parse_qs(urlparse.urlparse(referer).query)
            for key, value in search_params.items():
                utm_marks[key] = value[0]

        fields = []
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
        if installation_extension_settings.data.get('defaultStatus') != 'first':
            status = Status.query \
                .with_entities(Status.id) \
                .filter_by(nepkit_installation_id=installation_extension_settings.nepkit_installation_id,
                           id=installation_extension_settings.data.get('defaultStatus')) \
                .first()
        if installation_extension_settings.data.get('defaultStatus') == 'first' or not status:
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

        installation_settings = InstallationSettings.query \
            .filter_by(nepkit_installation_id=lead.nepkit_installation_id) \
            .first()
        if installation_settings.notifications_new_lead_extension_enabled:
            # Send notification
            fields_str = ''
            for field in Lead.get_fields(lead.id, for_api=True):
                fields_str += '{}: {} \r'.format(field['field_name'], field['value'])
            lead.send_notification(content={
                'en': 'New lead #{} \r{}'.format(lead.uid, fields_str),
                'ru': 'Новый лид #{} \r{}'.format(lead.uid, fields_str)
            })

        return '#{}'.format(lead.uid)