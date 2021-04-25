import os
from flask import request

from flaskr.models.installation_settings import InstallationSettings
from flaskr.models.lead import Lead
from flaskr import db
from flask_babel import _

from flaskr.models.lead import LeadAction, LeadActionType
from flaskr.models.status import Status
from flaskr.extensions.extension import Extension
from flaskr.views.view import compile_js, method_with_vars

settings_script = compile_js('settings_script')


# Wix extension
# https://www.wix.com/
class WixExtension(Extension):
    id = os.environ.get('WIX_INTEGRATION_ID')
    key = 'wix'
    with_settings = True

    def __init__(self):
        Extension.__init__(self)
        self.name = 'Wix'

    @staticmethod
    def get_default_data():
        return {
            'defaultStatus': 'first',
            'mapping': []
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

        fields_q = db.session.execute("""
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
        fields = []
        for field in fields_q:
            fields.append({
                'id': field['id'],
                'name': field['name']
            })

        print('installation_extension_settings.data', installation_extension_settings.data)

        wix_fields = [
            {'key': 'contact.Name.First', 'name': 'Имя контакта'},
            {'key': 'contact.Name.Middle', 'name': 'Отчество контакта'},
            {'key': 'contact.Name.Last', 'name': 'Фамилия контакта'},
            {'key': 'contact.Email[0]', 'name': 'Первая эл. почта контакта'},
            {'key': 'contact.Email[1]', 'name': 'Вторая эл. почта контакта'},
            {'key': 'contact.Email[2]', 'name': 'Третья эл. почта контакта'},
            {'key': 'contact.Phone[0]', 'name': 'Первый телефон контакта'},
            {'key': 'contact.Phone[1]', 'name': 'Второй телефон контакта'},
            {'key': 'contact.Phone[2]', 'name': 'Третий телефон контакта'},
            {'key': 'contact.Address[0].Country', 'name': 'Страна контакта'},
            {'key': 'contact.Address[0].Street', 'name': 'Улица контакта'},
            {'key': 'contact.Address[0].City', 'name': 'Город контакта'},
            {'key': 'contact.Address[0].Zip', 'name': 'Индекс контакта'}
        ]

        return {
            'strs': {
                'form_defaultStatus': _('e_wix_settings_form_defaultStatus'),
                'form_defaultStatus_alwaysFirst': _('e_wix_settings_form_defaultStatus_alwaysFirst'),
                'form_defaultStatus_required': _('e_wix_settings_form_defaultStatus_required'),
                'form_save': _('e_wix_settings_form_save'),
                'notification_changesSaved': _('e_wix_settings_notification_changesSaved')
            },
            'statuses': statuses,
            'fields': fields,
            'wixFields': wix_fields,
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
            field_keys_list += '- {} - `f{}` \r'.format(field['name'], field['id'])

        return [
            {
                '_com': 'Information',
                'content': _('v_extension_wix_information_content',
                             webhook_url='https://nepkit.team/atomcrm/ext/wix/wh/{}_{}'.format(
                                 installation_extension_settings.id, installation_extension_settings.token),
                             STATIC_URL=os.environ.get('STATIC_URL'),
                             field_keys_list=field_keys_list)
            },
            {
                '_com': 'Button',
                'icon': 'setting',
                'label': _('v_extension_wix_openSettings'),
                'to': ['extension', {'key': 'wix', 'tab': 'settings'}]
            }
        ]

    @staticmethod
    def catch_webhook(installation_extension_settings, webhook_key=None):
        data = request.get_json(force=True).get('data')

        fields = []
        mapping = installation_extension_settings.data['mapping']
        for mapping_field in mapping:
            field_key = mapping_field.get('key')
            field_id = mapping_field.get('field')
            field_value = data.get(field_key) if field_key else None

            if field_id and field_value:
                fields.append({
                    'field_id': field_id,
                    'value': field_value
                })

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
        # lead.utm_source = utm_marks.get('utm_source', None)
        # lead.utm_medium = utm_marks.get('utm_medium', None)
        # lead.utm_campaign = utm_marks.get('utm_campaign', None)
        # lead.utm_term = utm_marks.get('utm_term', None)
        # lead.utm_content = utm_marks.get('utm_content', None)

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
