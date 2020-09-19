from flaskr.views.view import View
from flaskr.models.lead import Lead
from flaskr.models.field import Field, FieldType
from flaskr.models.status import Status


content = """
### Search by ID:
```id=1```

### Show only archived leads:
```archived=true```

### Search lead by UTM marks"
- ```utm_source=google```
- ```utm_medium=cpc```
- ```utm_campaign=spring_sale```
- ```utm_term=running+shoes```
- ```utm_content=textlink```
"""

# Window: Search info
class SearchInfo(View):
    meta = {
        'name': 'Advanced search'
    }

    def get_header(self, params, request_data):
        return {
            'title': self.meta.get('name')
        }

    def get_schema(self, params, request_data):
        return [
            {
                '_com': 'Information',
                'content': content
            }
        ]
