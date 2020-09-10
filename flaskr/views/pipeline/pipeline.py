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
                    'toWindow': 'searchInfo',
                },
                # {
                #     '_com': 'Button',
                #     '_vis': len(self.statuses) > 0,
                #     'type': 'primary',
                #     'icon': 'plus',
                #     'label': 'New lead',
                #     'toWindow': 'createLead'
                # }
            ],
            'search': {
                'placeholder': 'Search...',
                'onSearch': 'onSearchLeads'
            }
        }

    def get_schema(self, params, request_data):
        board_columns = []

        for status in self.statuses:
            load_more_vis = False

            board_column_items = []
            for lead in status['leads']:
                board_column_items.append({
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

            board_columns.append({
                'key': status['id'],
                'title': status['name'],
                'count': status['lead_count'],
                'color': get_hex_by_color(status['color']),
                'showAdd': True,
                'onAdd': 'addLead',
                'showLoad': load_more_vis,
                'items': board_column_items,
                'onLoad': ['loadLeads', {
                    'statusId': status['id']
                }]
            })

        return [
            {
                '_com': 'Board',
                '_id': 'leadsBoard',
                'columns': board_columns
            }
        ]

    methods = {
        'addLead':
            """(app, params, event) => {
                const { columnKey, columnIndex } = event
                const page = app.getView()
                const board = page.getCom('leadsBoard')
                const boardColumns = board.getAttr('columns')
                
                // Set loading to add button
                boardColumns[columnIndex].addLoading = true
                board.setAttr('columns', boardColumns)
                
                app
                    .sendReq('createLead', {
                        statusId: columnKey
                    })
                    .then(result => {
                        if (result._res === 'ok') {
                            page.callMethod('loadLeads', {
                                byAdd: true,
                                statusId: columnKey,
                                showLoading: false
                            })
                        }
                    })
            }""",
        'loadLeads':
            """(app, params, event) => {
                const { statusId, offset, limit, byAdd=false } = params
                const page = app.getView()
                const board = page.getCom('leadsBoard')
                const boardItems = board.getAttr('items')
                const boardColumns = board.getAttr('columns')
                const boardColumn = boardColumns.find(c => c.key == statusId)
                
                app
                    .sendReq('getLeads', {
                        statusId,
                        offset,
                        limit
                    })
                    .then(result => {
                        if (result._res === 'ok') {
                            const { leads, total } = result
                            
                            // Unset loading to add button
                            boardColumn.addLoading = false
                            
                            // Delete items
                            boardColumn.count = total
                            boardColumn.items = leads.map(lead => ({
                                key: lead.id,
                                title: lead.title,
                                description: lead.description,
                                onClick
                            }))
                        
                            if (byAdd && statusId) {
                                board.setAttr('columns', boardColumns)
                            }
                        }
                    })
            }""",
        'onSearchLeads':
            """(app, params) => {
                
            }""",
        'onDragLead':
            """(app, params) => {

            }"""
    }
