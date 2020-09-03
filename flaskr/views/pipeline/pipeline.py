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
        self.statuses = Status.query \
            .filter_by(veokit_system_id=1) \
            .order_by(Status.index.asc()) \
            .all()

        for status in self.statuses:
            status.leads = Lead.query \
                .filter_by(veokit_system_id=1,
                           status_id=status.id)\
                .offset(0) \
                .limit(5) \
                .all()

    def get_header(self, params):
        return {
            'title': self.meta.get('name'),
            'actions': [
                {
                    '_com': 'Button',
                    'type': 'solid',
                    'icon': 'infoCircle',
                    'toWindow': 'searchSyntax'
                },
                {
                    '_com': 'Button',
                    'type': 'primary',
                    'icon': 'plus',
                    'label': 'Add lead',
                    'toWindow': 'createLead'
                }
            ],
            'search': {
                'placeholder': 'Search...',
                'onSearch': 'onSearchLeads'
            }
        }

    def get_schema(self, params):
        board_columns = []
        board_items = []

        for status in self.statuses:
            load_more_vis = False
            board_columns.append({
                'key': status.id,
                'title': status.name,
                'subtitle': '{} {}'.format(23, 'lead' if 23 == 1 else 'leads'),
                # 'color': status.color,
                'loadMore': load_more_vis,
                'onLoadMore': 'loadMireItems'
            })

            for lead in status.leads:
                board_items.append({
                    'key': lead.id,
                    'columnKey': status.id,
                    'title': 'Lead title',
                    'description': 'Lead description...',
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
                'columns': board_columns,
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
