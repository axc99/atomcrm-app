from flaskr.views.view import View
from flaskr.models.lead import Lead
from flaskr.models.status import Status


# Page: Pipeline
class Pipeline(View):
    meta = {
        'name': 'Leads'
    }

    leads = []
    statuses = []

    def before(self, params):
        self.leads = Lead.query \
            .filter_by(veokit_system_id=1) \
            .all()
        self.statuses = Status.query \
            .filter_by(veokit_system_id=1) \
            .order_by(Status.index.asc()) \
            .all()

    def get_header(self, params):
        return {
            'title': self.meta.get('name'),
            'actions': [
                {
                    '_com': 'Field.Input',
                    'multiple': True,
                    'placeholder': 'Enter tags'
                }
            ],
            'search': {
                'placeholder': 'Search...',
                'onSearch': 'onSearchLeads'
            }
        }

    def get_schema(self, params):
        board_rows = []
        for status in self.statuses:
            board_rows.append({
                'id': status.id,
                'title': [
                    {
                        '_com': 'Badge',
                        'dot': True,
                        'color': 'red',
                        'text': status.name
                    }
                ],
                'subtitle': '{} {}'.format(23, 'lead' if 23 == 1 else 'leads')
            })

        board_items = []
        for lead in self.leads:
            board_items.append({
                'id': lead.id,
                'title': lead.title,
                'description': 'max three random fields here',
                'extra': [
                    'Added on 12 Jun at 11:34',
                    {
                        '_com': 'Tags',
                        'tags': [
                            'firstTag',
                            'secondTag'
                        ]
                    }
                ]
            })

        return [
            {
                '_com': 'Board',
                'rows': board_rows,
                'items': board_items
            }
        ]

    methods = {
        'onEnterTags':
            """(app, params) => {
                
            }""",
        'onSearchLeads':
            """(app, params) => {
                
            }""",
        'onDragLead':
            """(app, params) => {

            }""",
        'archiveLead':
            """(app, params) => {

            }"""
    }
