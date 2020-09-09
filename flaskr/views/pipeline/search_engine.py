from flaskr.views.view import View
from flaskr.models.lead import Lead
from flaskr.models.field import Field, FieldType
from flaskr.models.status import Status


# Window: Search engine
class SearchEngine(View):
    meta = {
        'name': 'Search Engine'
    }

    def get_header(self, params, request_data):
        return {
            'title': self.meta.get('name')
        }

    def get_schema(self, params, request_data):
        return [
            {
                '_com': 'Information',
                'content': """
                    ## Search by ID:
                    ```id=1```
                    
                    ## Show only archived leads
                    ```archived=true```
                    
                    ## Search lead by first name
                    ```firstName=ABC```
                """
            }
        ]
