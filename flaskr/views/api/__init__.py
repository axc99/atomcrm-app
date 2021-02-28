import os
from flask_babel import _

from flaskr.models.status import Status
from flaskr.models.task import Task
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
                'name': _('v_api_name'),
                'tokenModal_title': _('v_tokenModal_title'),
                'tokenModal_subtitle': _('v_tokenModal_subtitle'),
                'tokenModal_createToken': _('v_tokenModal_createToken'),
                'tokenModal_token': _('v_tokenModal_token')
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

            statuses = Status.query.filter_by(nepkit_installation_id=request_data['installation_id']) \
                .order_by(Status.index.asc()) \
                .limit(500)\
                .all()
            content_table = ''
            for status in statuses:
                content_table += '- {}: `{}` \r'.format(status.name, status.id)
            content = content.format(content_table)

        elif tab == 'fields':
            content = open(os.path.join(dirname, './pages/fields.md'), 'r').read()

            fields = Field.query.filter_by(nepkit_installation_id=request_data['installation_id']) \
                .order_by(Field.index.asc()) \
                .limit(500) \
                .all()
            content_table = ''
            for field in fields:
                content_table += '- {}: `{}` \r'.format(field.name, field.id)
            content = content.format(content_table)

        elif tab == 'tasks':
            content = open(os.path.join(dirname, './pages/tasks.md'), 'r').read()

            tasks = Task.query.filter_by(nepkit_installation_id=request_data['installation_id']) \
                .order_by(Task.index.asc()) \
                .limit(500) \
                .all()
            content_table = ''
            for task in tasks:
                content_table += '- {}: `{}` \r'.format(task.name, task.id)
            content = content.format(content_table)

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
                },
                {
                    'key': 'tasks',
                    'text': _('v_api_header_tabs_tasks'),
                    'to': {
                        'tab': 'tasks'
                    }
                }
            ]
        }
