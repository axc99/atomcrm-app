from flask_babel import _

from flaskr.views.view import View, get_method
from flaskr.models.status import Status, get_status_colors

compiled_methods = {
    'onFinishForm': get_method('methods/onFinishForm')
}


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
                'onFinish': 'onFinishForm',
                'fields': [
                    {
                        '_com': 'Field.Input',
                        'type': 'text',
                        'key': 'name',
                        'label': _('v_createStatus_form_name'),
                        'placeholder': _('v_createStatus_form_name_placeholder'),
                        'maxLength': 30,
                        'rules': [
                            {'max': 30, 'message': _('v_createStatus_name_length')},
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

    methods = compiled_methods
