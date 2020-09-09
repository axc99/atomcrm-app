from flaskr import db
from flaskr.views.view import View
from flaskr.models.lead import Lead
from flaskr.models.status import Status, get_hex_by_color


# Page: Pipeline
class Pipeline(View):
    meta = {
        'name': 'Leads'
    }

    leads = []
    statuses = []

    def before(self, params, request_data):
        self.statuses = []

        statuses_q = db.session.execute("""  
            SELECT 
                s.*,
                (SELECT COUNT(*) FROM public.lead AS l WHERE l.status_id = s.id) AS lead_count
            FROM 
                public.status AS s
            WHERE
                s.veokit_installation_id = :installation_id
            ORDER BY 
                s.index""", {
            'installation_id': request_data['installation_id']
        })

        for status in statuses_q:
            status_leads = Lead.query \
                .filter_by(veokit_installation_id=request_data['installation_id'],
                           status_id=status['id']) \
                .offset(0) \
                .limit(5) \
                .all()

            self.statuses.append({
                'id': status['id'],
                'name': status['name'],
                'lead_count': status['lead_count'],
                'color': status['color'],
                'leads': status_leads
            })

    def get_header(self, params, request_data):
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
                    '_vis': len(self.statuses) > 0,
                    'type': 'primary',
                    'icon': 'plus',
                    'label': 'New lead',
                    'toWindow': 'createLead'
                }
            ],
            'search': {
                'placeholder': 'Search...',
                'onSearch': 'onSearchLeads'
            }
        }

    def get_schema(self, params, request_data):
        board_columns = []
        board_items = []

        for status in self.statuses:
            load_more_vis = False
            board_columns.append({
                'key': status['id'],
                'title': status['name'],
                'count': status['lead_count'],
                'color': get_hex_by_color(status['color']),
                'showLoadBtn': load_more_vis,
                'onLoad': ['loadLeads', {
                    'statusId': status['id']
                }]
            })

            for lead in status['leads']:
                board_items.append({
                    'toWindow': ['updateLead', {
                        'id': lead.id
                    }],
                    'key': lead.id,
                    'columnKey': status['id'],
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
        'loadLeads':
            """(app, params) => {
                
            }""",
        'onSearchLeads':
            """(app, params) => {
                
            }""",
        'onDragLead':
            """(app, params) => {

            }"""
    }
