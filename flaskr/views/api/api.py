import os

from flaskr.views.view import View
from flaskr.models.field import Field, FieldType


# Page: Api
class Api(View):
    meta = {
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
                    'label': 'Get token',
                    'toWindow': 'getToken'
                }
            ],
            'tabs': [
                {
                    'key': 'leads',
                    'text': 'Leads',
                    'to': {
                        'tab': None
                    }
                },
                {
                    'key': 'statuses',
                    'text': 'Statuses',
                    'to': {
                        'tab': 'statuses'
                    }
                },
                {
                    'key': 'fields',
                    'text': 'Fields',
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

    methods = {
        'onSortFields':
            """(app, params) => {

            }""",
        'deleteField':
            """(app, params) => {

            }"""
    }
