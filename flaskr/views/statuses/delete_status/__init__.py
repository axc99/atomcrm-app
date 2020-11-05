from flask_babel import _
from cerberus import Validator

from flaskr.views.view import View, get_method, method_with_vars
from flaskr.models.status import Status, get_hex_by_color

compiled_methods = {
    'onFinishForm': get_method('methods/onFinishForm')
}


# Window: Delete status
# If leads with deleted status exist
class DeleteStatus(View):
    def __init__(self):
        self.meta = {
            'name': _('v_deleteStatus_meta_name')
        }
        self.deleted_status = None
        self.other_statuses = []

    def before(self, params, request_data):
        vld = Validator({
            'id': {'type': 'number', 'required': True}
        })
        is_valid = vld.validate(params)
        if not is_valid:
            raise Exception({'message': 'Invalid params',
                             'errors': vld.errors})

        self.deleted_status = Status.query \
            .filter_by(id=params['id'],
                       veokit_installation_id=request_data['installation_id']) \
            .first()
        if not self.deleted_status:
            raise Exception()

        self.other_statuses = Status.query \
            .filter(Status.veokit_installation_id == request_data['installation_id'],
                    Status.id != params['id']) \
            .order_by(Status.index.asc()) \
            .all()

    def get_header(self, params, request_data):
        return {
            'title': self.meta.get('name'),
            'subtitle': _('v_deleteStatus_header_subtitle', status_name=self.deleted_status.name)
        }

    def get_schema(self, params, request_data):
        select_options = [
            {
                'key': 'deleteLeads',
                'label': _('v_deleteStatus_schema_form_action_deleteLeads')
            }
        ]

        for status in self.other_statuses:
            select_options.append({
                'key': status.id,
                'color': get_hex_by_color(status.color.name),
                'label': _('v_deleteStatus_schema_form_action_moveLeads', status_name=status.name)
            })

        return [
            {
                '_com': 'Form',
                '_id': 'deleteStatusForm',
                'onFinish': 'onFinishForm',
                'fields': [
                    {
                        '_com': 'Field.Select',
                        'key': 'action',
                        'value': select_options[0]['key'] if len(select_options) > 0 else 'deleteLeads',
                        'options': select_options
                    }
                ],
                'buttons': [
                    {
                        '_com': 'Button',
                        'type': 'danger',
                        'submitForm': True,
                        'label': _('v_deleteStatus_schema_form_btn')
                    }
                ]
            }
        ]

    def get_methods(self, params, request_data):
        methods = compiled_methods.copy()

        methods['onFinishForm'] = method_with_vars(methods['onFinishForm'], {'STATUS_ID': self.deleted_status.id})

        return methods
