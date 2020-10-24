import os
from flaskr import db
from flask_babel import _
from flaskr.views.extensions.extensions.extension import Extension


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
            field_keys_list += '- {}: `f{}` \r'.format(field['name'], field['id'])

        return [
            {
                '_com': 'Information',
                'content': _('v_extension_tilda_information_content',
                             webhook_url='https://veokit.team/atomcrm/ext/tilda/wh/{}_{}'.format(installation_extension_settings.id, installation_extension_settings.token),
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
                s.veokit_installation_id = :veokit_installation_id
            ORDER BY 
                s.index""", {
            'veokit_installation_id': request_data['installation_id']
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

    def get_methods_for_settings(self, installation_extension_settings, params, request_data):
        return {
            'onFinishForm':
                """(app, args, event) => {
                    const window = app.getView()
                    const form = window.getCom('extensionSettingsForm')
                    const { values } = event

                    form.setAttr('loading', true)

                    app
                        .sendReq('updateExtensionSettings', {
                            extensionId: """ + str(installation_extension_settings.id) + """,
                            data: values
                        })
                        .then(result => {
                            form.setAttr('loading', false)
                        })
                }"""
        }
