import os
from flaskr import db
from flask_babel import _
from flaskr.views.extensions.extensions.extension import Extension


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
            'default_status': 'first'
        }

    def get_schema_for_information(self, installation_extension_settings, params, request_data):
        fields = db.session.execute("""
                    SELECT 
                        f.*
                    FROM 
                        public.field AS f
                    WHERE
                        f.veokit_installation_id = :veokit_installation_id
                    ORDER BY 
                        f.index""", {
            'veokit_installation_id': request_data['installation_id']
        })

        # Create markdown field-key list
        field_keys_list = ''
        for field in fields:
            field_keys_list += '- {} - `f{}` \r'.format(field['name'], field['id'])

        return [
            {
                '_com': 'Information',
                'content': _('v_extension_wix_information_content',
                             webhook_url='https://veokit.team/atomcrm/ext/wix/wh/{}_{}'.format(installation_extension_settings.id, installation_extension_settings.token),
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

    def get_schema_for_settings(self, installation_extension_settings, params, request_data):
        statuses = db.session.execute("""
            SELECT 
                s.*,
                (SELECT COUNT(*) FROM public.lead AS l WHERE l.status_id = s.id AND l.archived = false) AS lead_count
            FROM 
                public.status AS s
            WHERE
                s.veokit_installation_id = :veokit_installation_id
            ORDER BY 
                s.index""", {
            'veokit_installation_id': request_data['installation_id']
        })

        status_options = [
            {'value': 'first', 'label': _('v_extension_wix_information_settings_status_alwaysFirst')}
        ]
        for status in statuses:
            status_options.append({
                'value': status.id,
                'color': status.color,
                'label': status.name
            })

        fields = db.session.execute("""
                            SELECT 
                                f.*
                            FROM 
                                public.field AS f
                            WHERE
                                f.veokit_installation_id = :veokit_installation_id
                            ORDER BY 
                                f.index""", {
            'veokit_installation_id': request_data['installation_id']
        })
        field_options = [
            {'value': 0, 'label': 'Не указано'}
        ]
        for field in fields:
            field_options.append({
                'value': field['id'], 'label': field['name']
            })

        table_rows = []
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

        mapping = installation_extension_settings.data['mapping']
        for wix_field in wix_fields:
            mapping_value = next((r.get('field') for r in mapping if r.get('key') == wix_field['key']), 0)
            table_rows.append({
                'key': wix_field['key'],
                'wixField': wix_field['name'],
                'field': {
                    '_com': 'Field.Select',
                    'value': mapping_value,
                    'options': field_options
                }
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
                        'label': _('v_extension_wix_information_settings_status'),
                        'options': status_options,
                        'value': installation_extension_settings.data.get('default_status'),
                        'rules': [
                            {'required': True,
                             'message': _('v_extension_wix_information_settings_primary_rules_required')}
                        ]
                    },
                    {
                        '_com': 'Field.Custom',
                        'columnWidth': 8,
                        'label': 'Соотношение полей',
                        'content': [
                            {
                                '_com': 'Table',
                                '_id': 'extensionSettingsForm_mapping_table',
                                'columns': [
                                    {
                                        'width': 50,
                                        'key': 'wixField',
                                        'title': 'Поле в Wix'
                                    },
                                    {
                                        'width': 50,
                                        'key': 'field',
                                        'title': 'Поле в AtomCRM'
                                    }
                                ],
                                'rows': table_rows
                            }
                        ]
                    }
                ],
                'buttons': [
                    {
                        '_com': 'Button',
                        'type': 'primary',
                        'submitForm': True,
                        'icon': 'save',
                        'label': _('v_extension_wix_information_settings_save')
                    }
                ]
            }
        ]

    def get_methods_for_settings(self, installation_extension_settings, params, request_data):
        return {
            'onFinishForm':
                """(app, args, event) => {
                    const page = app.getPage()
                    const form = page.getCom('extensionSettingsForm')
                    const mappingTable = page.getCom('extensionSettingsForm_mapping_table')
                    const rows = mappingTable.getAttr('rows')
                    const { values } = event
                    
                    const data = {
                        ...values,
                        mapping: []
                    }
                    rows.map(row => {
                        data.mapping.push({
                            key: row.key,
                            field: row.field.value
                        })
                    })

                    form.setAttr('loading', true)
                    app
                        .sendReq('updateExtensionSettings', {
                            extensionId: """ + str(installation_extension_settings.id) + """,
                            data
                        })
                        .then(result => {
                            form.setAttr('loading', false)
                        })
                }"""
        }
