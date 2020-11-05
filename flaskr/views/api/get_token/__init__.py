from flask_babel import _
from flaskr.views.view import View, get_method
from flaskr.models.field import Field, FieldType

compiled_methods = {
    'getToken': get_method('methods/getToken')
}


# Window: Get token
class GetToken(View):
    def __init__(self):
        self.meta = {
            'name': _('v_getToken_meta_name')
        }

    def get_header(self, params, request_data):
        return {
            'title': self.meta.get('name'),
            'subtitle': _('v_getToken_meta_header_subtitle')
        }

    def get_schema(self, params, request_data):
        return [
            {
                '_id': 'getTokenBtn',
                '_com': 'Button',
                'type': 'primary',
                'label': _('v_getToken_schema_btn'),
                'onClick': 'getToken'
            },
            {
                '_id': 'tokenInput',
                '_com': 'Field.Input',
                '_vis': False,
                'label': _('v_getToken_schema_token'),
                'multiline': True,
                'type': 'text',
                'readOnly': True
            }
        ]

    methods = compiled_methods
