from flaskr.views.view import View
from flask_babel import _
from flaskr.models.lead import Lead
from flaskr.models.field import Field, FieldType
from flaskr.models.status import Status


# Window: Search info
class SearchInfo(View):
    def __init__(self):
        self.meta = {
            'name': _('v_searchInfo_meta_name')
        }
        self.content = _('v_searchInfo_content')

    def get_header(self, params, request_data):
        return {
            'title': self.meta.get('name')
        }

    def get_schema(self, params, request_data):
        return [
            {
                '_com': 'Information',
                'content': self.content
            }
        ]
