import os
from flask_babel import _

from flaskr.views.view import View
from flaskr.models.field import Field, FieldType


# Page: API
class Api(View):
    def __init__(self):
        self.meta = {
            'name': 'API'
        }

    def get_header(self, params, request_data):
        return {
            'title': self.meta.get('name'),
            'actions': [
                {
                    '_com': 'Button',
                    'type': 'primary',
                    'icon': 'lock',
                    'label': _('v_api_header_getToken'),
                    'toWindow': 'getToken'
                }
            ],
            'tabs': [
                {
                    'key': 'leads',
                    'text': _('v_api_header_tabs_leads'),
                    'to': {
                        'tab': None
                    }
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

    def get_schema(self, params, request_data):
        content = ''
        dirname = os.path.dirname(__file__)
        tab = params.get('tab')

        if not tab or tab == 'leads':
            content = open(os.path.join(dirname, './pages/leads.md'), 'r').read()
        elif tab == 'statuses':
            content = open(os.path.join(dirname, './pages/statuses.md'), 'r').read()
        elif tab == 'fields':
            content = open(os.path.join(dirname, './pages/fields.md'), 'r').read()

        return [
            {
                '_com': 'Information',
                'content': content
            }
        ]
