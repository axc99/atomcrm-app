from flask_babel import _
from cerberus import Validator

from flaskr.views.view import View, get_method, method_with_vars
from flaskr.models.status import Status, get_status_colors

compiled_methods = {
    'onFinishForm': get_method('methods/onFinishForm')
}


# Window: Update status
class UpdateStatus(View):
    def __init__(self):
        self.meta = {
            'name': _('v_updateStatus_meta_name')
        }
        self.status = None

    def before(self, params, request_data):
        vld = Validator({
            'id': {'type': 'number', 'required': True}
        })
        is_valid = vld.validate(params)
        if not is_valid:
            raise Exception({'message': 'Invalid params',
                             'errors': vld.errors})

        self.status = Status.query\
                            .filter_by(id=params['id'],
                                       nepkit_installation_id=request_data['installation_id'])\
                            .first()
        if not self.status:
            raise Exception()

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
                '_id': 'updateStatusForm',
                'onFinish': 'onFinishForm',
                'fields': [
                    {
                        '_com': 'Field.Input',
                        'type': 'text',
                        'key': 'name',
                        'label': _('v_updateStatus_form_name'),
                        'placeholder': _('v_updateStatus_form_name_placeholder'),
                        'maxLength': 30,
                        'rules': [
                            {'max': 30, 'message': _('v_updateStatus_name_length')},
                            {'required': True, 'message': _('v_updateStatus_name_required')}
                        ],
                        'value': self.status.name
                    },
                    {
                        '_com': 'Field.Select',
                        'value': 'red',
                        'key': 'color',
                        'label': _('v_updateStatus_form_color'),
                        'options': color_options,
                        'value': self.status.color.name,
                        'rules': [
                            {'required': True, 'message': _('v_updateStatus_form_color_required')}
                        ]
                    }
                ],
                'buttons': [
                    {
                        '_com': 'Button',
                        'type': 'primary',
                        'submitForm': True,
                        'icon': 'save',
                        'label': _('v_updateStatus_btn')
                    }
                ]
            }
        ]

    def get_methods(self, params, request_data):
        methods = compiled_methods.copy()

        methods['onFinishForm'] = method_with_vars(methods['onFinishForm'], {'STATUS_ID': self.status.id})

        return methods
