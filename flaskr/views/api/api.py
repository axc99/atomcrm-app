from flaskr.views.view import View
from flaskr.models.field import Field, FieldType


# Page: Api
class Api(View):
    meta = {
        'name': 'API'
    }

    def get_header(self, params):
        return {
            'title': self.meta.get('name'),
            'actions': [
                {
                    '_com': 'Button',
                    'type': 'danger',
                    'label': 'Get new token',
                    'toWindow': 'createNewToken'
                }
            ],
            'tabs': [
                {
                    'key': 'leads',
                    'title': 'Leads',
                    'to': {
                        'tab': None
                    }
                },
                {
                    'key': 'statuses',
                    'title': 'Statuses',
                    'to': {
                        'tab': 'statuses'
                    }
                },
                {
                    'key': 'fields',
                    'title': 'Fields',
                    'to': {
                        'tab': 'fields'
                    }
                }
            ]
        }

    def get_schema(self, params):
        content = ''

        if not params.tab or params.tab == 'leads':
            content = open('pages/leads.md', 'r').read()
        elif params.tab == 'statuses':
            content = open('pages/statuses.md', 'r').read()
        elif params.tab == 'fields':
            content = open('pages/fields.md', 'r').read()

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
