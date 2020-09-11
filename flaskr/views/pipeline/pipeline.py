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

        self.statuses = []
        for status in statuses_q:
            leads_q = db.session.execute("""  
                SELECT 
                    l.*
                FROM 
                    public.lead AS l
                WHERE
                    l.veokit_installation_id = :installation_id AND
                    l.status_id = :status_id
                ORDER BY 
                    l.add_date DESC
                OFFSET 
                    0
                LIMIT
                    5""", {
                'installation_id': request_data['installation_id'],
                'status_id': status['id']
            })

            status_leads = []
            for lead in leads_q:
                status_leads.append({
                    'id': lead.id,
                    'status_id': lead.status_id,
                    'fields': Lead.get_fields(lead.id),
                    'tags': Lead.get_tags(lead.id)
                })

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
                }
            ],
            'search': {
                'placeholder': 'Search...',
                'onSearch': 'onSearchLeads'
            }
        }

    def get_schema(self, params, request_data):
        board_columns = []

        for status in self.statuses:
            board_column_items = []

            for lead in status['leads']:
                board_column_items.append(get_lead_component(lead))

            board_columns.append({
                'key': status['id'],
                'title': status['name'],
                'count': status['lead_count'],
                'color': get_hex_by_color(status['color']),
                'items': board_column_items,
                'showAdd': True,
                'onAdd': 'addLead',
                'showLoad': status['lead_count'] > 5,
                'onLoad': ['loadLeads', {
                    'statusId': status['id']
                }]
            })

        return [
            {
                '_com': 'Board',
                '_id': 'leadsBoard',
                'draggable': True,
                'onDrag': 'onDragLead',
                'columns': board_columns
            }
        ]

    methods = {
        # Add lead to status
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
                            // Update leads in column
                            app
                                .sendReq('getLeadComponents', {
                                    statusId: columnKey,
                                    offset: 0,
                                    limit: 5
                                })
                                .then(result => {
                                    // Unset loading to add button
                                    boardColumns[columnIndex].addLoading = false
                                    board.setAttr('columns', boardColumns)
                                    
                                    if (result._res == 'ok') {
                                        const { leadComponents, leadTotal } = result
                                    
                                        // Set count and set/append items
                                        boardColumns[columnIndex].count = leadTotal
                                        boardColumns[columnIndex].items = leadComponents
                                        
                                        board.setAttr('columns', boardColumns)
                                    }
                                })
                        }
                    })
            }""",

        # Load leads by status
        'loadLeads':
            """(app, params, event) => {
                const { columnKey, columnIndex } = event
                const { statusId, byAdd=false } = params
                const page = app.getView()
                const board = page.getCom('leadsBoard')
                const boardColumns = board.getAttr('columns')
                
                // Set loading to load button
                boardColumns[columnIndex].loadLoading = true
                board.setAttr('columns', boardColumns)
                
                app
                    .sendReq('getLeadComponents', {
                        statusId,
                        offset: boardColumns[columnIndex].items.length,
                        limit: 5
                    })
                    .then(result => {
                        // Unset loading to load button
                        boardColumns[columnIndex].loadLoading = false
                        board.setAttr('columns', boardColumns)
                            
                        if (result._res === 'ok') {
                            const { leadComponents, leadTotal } = result
                            
                            // Set count and set/append items
                            boardColumns[columnIndex].count = leadTotal
                            boardColumns[columnIndex].items = byAdd ? leadComponents : [
                                ...boardColumns[columnIndex].items,
                                ...leadComponents
                            ]
                            
                            // If there are no leads left then hide load button
                            boardColumns[columnIndex].showLoad = boardColumns[columnIndex].items.length < leadTotal
                            
                            board.setAttr('columns', boardColumns)
                        }
                    })
            }""",

        # Drag lead between statuses
        'onDragLead':
            """(app, params, event) => {
                const { oldColumnIndex, newColumnIndex, newColumnKey, oldItemIndex, newItemIndex } = event
                const page = app.getView()
                const board = page.getCom('leadsBoard')
                const boardColumns = board.getAttr('columns')
                
                // Get item from old column
                const item = boardColumns[oldColumnIndex].items[oldItemIndex]
                
                // Add item new column
                // boardColumns[oldColumnIndex].items.slice(newItemIndex, 0, item)
                
                // Remove item from column
                boardColumns[oldColumnIndex].items.slice(oldItemIndex, 1)
                
                // Update columns on board
                board.setAttr('columns', boardColumns)
                
                app.sendReq('updateLead', {
                    id: key,
                    statusId: newColumnKey
                })
            }"""
    }


# Get lead component
def get_lead_component(lead):
    title = ''
    description = []
    for field in lead['fields']:
        if field['field_value_type'] in ('number', 'string'):
            if field['field_as_title']:
                title += field['value'] + ' '
            elif field['field_primary']:
                description.append(field['value'])
    title = title.strip()

    return {
        'key': lead['id'],
        'columnKey': lead['status_id'],
        'title': title if title else 'No name',
        'description': description if len(description) > 0 else 'Empty lead',
        'extra': [
            'Added on 12 Jun at 11:34',
            {
                '_com': 'Tags',
                'tags': [
                    'firstTag',
                    'secondTag'
                ]
            }
        ],
        'toWindow': ['updateLead', {
            'id': lead['id']
        }]
    }
