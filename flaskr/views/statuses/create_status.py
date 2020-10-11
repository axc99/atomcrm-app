from flask_babel import _

from flaskr.views.view import View
from flaskr.models.status import Status, get_status_colors


# Window: Create status
class CreateStatus(View):
    def __init__(self):
        self.meta = {
            'name': _('v_createStatus_meta_name')
        }

    def get_header(self, params, request_data):
        return {
            'title': self.meta.get('name')
        }

    def get_schema(self, params, request_data):
        status_colors = get_status_colors()
        color_options = []
        for c in status_colors:
            color_options.append({'value': c[1], 'label': c[3], 'color': c[2]})

        return [
            {
                '_com': 'Form',
                '_id': 'createStatusForm',
                'onFinish': 'onFinish',
                'fields': [
                    {
                        '_com': 'Field.Input',
                        'type': 'text',
                        'key': 'name',
                        'label': _('v_createStatus_form_name'),
                        'placeholder': _('v_createStatus_form_name_placeholder'),
                        'maxLength': 20,
                        'rules': [
                            {'min': 2, 'max': 20, 'message': _('v_createStatus_name_length')},
                            {'required': True, 'message': _('v_createStatus_name_required')}
                        ]
                    },
                    {
                        '_com': 'Field.Select',
                        'value': 'red',
                        'key': 'color',
                        'label': _('v_createStatus_form_color'),
                        'options': color_options,
                        'rules': [
                            {'required': True, 'message': _('v_createStatus_form_color_required')}
                        ]
                    }
                ],
                'buttons': [
                    {
                        '_com': 'Button',
                        'type': 'primary',
                        'submitForm': True,
                        'icon': 'plus',
                        'label': _('v_createStatus_btn')
                    }
                ]
            }
        ]

    methods = {
        'onFinish':
            """(app, params, event) => {
                const window = app.getView()
                const form = window.getCom('createStatusForm')
                const { values } = event
                
                form.setAttr('loading', true)
                
                app
                    .sendReq('createStatus', {
                        name: values.name,
                        color: values.color
                    })
                    .then(result => {
                        form.setAttr('loading', false)
                        
                        if (result.res == 'ok') {
                            // Reload parent page
                            app.getPage().reload()
                        }
                    })
            }"""
    }
