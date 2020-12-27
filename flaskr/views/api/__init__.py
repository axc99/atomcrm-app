import os
from flask_babel import _

from flaskr.views.view import View, compile_js
from flaskr.models.field import Field, FieldType

script = compile_js('script')


# Page: API
class Api(View):
    def __init__(self):
        self.script = script
        self.meta = {
            'name': 'API'
        }
        self.data = {
            'content': '',
            'strs': {
                'schema_tokenModal_title': _('v_getToken_meta_name'),
                'schema_tokenModal_subtitle': _('v_getToken_meta_header_subtitle'),
                'schema_tokenModal_btn': _('v_getToken_schema_btn'),
                'schema_tokenModal_token': _('v_getToken_schema_token')
            }
        }

    def before(self, params, request_data):
        content = ''
        dirname = os.path.dirname(__file__)
        tab = params.get('tab')

        if not tab or tab == 'leads':
            content = open(os.path.join(dirname, './pages/leads.md'), 'r').read()
        elif tab == 'statuses':
            content = open(os.path.join(dirname, './pages/statuses.md'), 'r').read()
        elif tab == 'fields':
            content = open(os.path.join(dirname, './pages/fields.md'), 'r').read()

        self.data['content'] = content

    def get_header(self, params, request_data):
        return {
            'title': self.meta.get('name'),
            'actions': [
                {
                    '_com': 'Button',
                    'icon': 'appstoreAdd',
                    'label': _('v_api_header_extensions'),
                    'to': ['control', {'tab': 'extensions'}]
                },
                {
                    '_com': 'Button',
                    'type': 'primary',
                    'icon': 'lock',
                    'label': _('v_api_header_getToken'),
                    'onClick': 'openToken'
                }
            ],
            'tabs': [
                {
                    'key': 'leads',
                    'text': _('v_api_header_tabs_leads'),
                    'to': {}
                },
                {
                    'key': 'statuses',
                    'text': _('v_api_header_tabs_statuses'),
                    'to': {
                        'tab': 'statuses'
                    }
                },
                {
                    'key': 'fields',
                    'text': _('v_api_header_tabs_fields'),
                    'to': {
                        'tab': 'fields'
                    }
                }
            ]
        }
