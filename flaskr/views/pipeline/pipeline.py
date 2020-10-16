from datetime import timedelta
from flask_babel import _

from flaskr import db
from flaskr.views.view import View
from flaskr.models.lead import Lead
from flaskr.models.status import Status, get_hex_by_color
from flaskr.models.installation_card_settings import InstallationCardSettings


# Page: Pipeline
class Pipeline(View):
    def __init__(self):
        self.leads = []
        self.statuses = []
        self.meta = {
            'name': _('v_pipeline_meta_name')
        }
        self.installation_card_settings = None

    def before(self, params, request_data):
        self.installation_card_settings = InstallationCardSettings.query \
            .filter_by(veokit_installation_id=request_data['installation_id']) \
            .first()

        statuses_q = db.session.execute("""  
            SELECT 
                s.*,
                (SELECT COUNT(*) FROM public.lead AS l WHERE l.status_id = s.id AND l.archived = false) AS lead_count,
                123456 AS lead_amount_sum
            FROM 
                public.status AS s
            WHERE
                s.veokit_installation_id = :installation_id
            ORDER BY 
                s.index""", {
            'installation_id': request_data['installation_id'],
            'amount_enabled': self.installation_card_settings.amount_enabled
        })

        self.statuses = []
        for status in statuses_q:
            leads_q = Lead.get_with_filter(installation_id=request_data['installation_id'],
                                           status_id=status['id'],
                                           search=params.get('search'),
                                           offset=0,
                                           limit=10,
                                           period_from=params.get('periodFrom'),
                                           period_to=params.get('periodTo'))

            status_leads = []
            status_lead_total = 0
            status_lead_amount_sum = 0

            for lead in leads_q:
                if status_lead_total == 0:
                    status_lead_total = lead.total
                if status_lead_amount_sum == 0:
                    status_lead_amount_sum = lead.amount_sum

                status_leads.append({
                    'id': lead.id,
                    'uid': lead.uid,
                    'status_id': lead.status_id,
                    'amount': lead.amount,
                    'archived': lead.archived,
                    'add_date': (lead.add_date + timedelta(minutes=request_data['timezone_offset'])).strftime('%Y-%m-%d %H:%M:%S'),
                    'fields': Lead.get_fields(lead.id),
                    'tags': Lead.get_tags(lead.id)
                })

            self.statuses.append({
                'id': status['id'],
                'name': status['name'],
                'lead_count': status_lead_total,
                'lead_amount_sum': status_lead_amount_sum,
                'color': status['color'],
                'leads': status_leads
            })

    def get_header(self, params, request_data):
        return {
            'title': self.meta.get('name'),
            'actions': [
                {
                    '_com': 'Button',
                    'icon': 'infoCircle',
                    'toWindow': 'searchInfo'
                },
                {
                    '_com': 'Field.DatePicker',
                    'range': True,
                    'allowClear': True,
                    'format': 'YYYY.MM.DD',
                    'onChange': 'onChangePeriod'
                }
            ],
            'search': {
                'placeholder': _('v_pipeline_header_search'),
                'onSearch': 'onSearchLeads'
            }
        }

    def get_schema(self, params, request_data):
        board_columns = []

        for status in self.statuses:
            board_column_items = []

            for lead in status['leads']:
                lead_component = get_lead_component(lead,
                                                    installation_card_settings=self.installation_card_settings)
                board_column_items.append(lead_component)

            board_columns.append({
                'key': status['id'],
                'title': status['name'],
                'subtitle': self.installation_card_settings.format_amount(status['lead_amount_sum']) if self.installation_card_settings.amount_enabled else None,
                'color': get_hex_by_color(status['color']),
                'items': board_column_items,
                'showAdd': False if (
                            params.get('search') or params.get('periodFrom') or params.get('periodTo')) else True,
                'onAdd': 'addLead',
                'total': status['lead_count'],
                'loadLimit': 10,
                'onLoad': ['loadLeads', {
                    'statusId': status['id'],
                    'addToEnd': True
                }]
            })

        return [
            {
                '_com': 'Board',
                '_id': 'leadsBoard',
                'draggableBetweenColumns': True,
                'onDrag': 'onDragLead',
                'columns': board_columns
            }
        ]

    def get_methods(self, params, request_data):
        return {
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
                            statusId: +columnKey
                        })
                        .then(result => {
                            if (result.res === 'ok') {
                                // Update leads in column
                                app
                                    .sendReq('getLeadComponents', {
                                        statusId: +columnKey,
                                        offset: 0,
                                        limit: 10
                                    })
                                    .then(result => {
                                        // Unset loading to add button
                                        boardColumns[columnIndex].addLoading = false
                                        board.setAttr('columns', boardColumns)

                                        if (result.res == 'ok') {
                                            const { leadComponents, leadTotal } = result

                                            // Set total and set/append items
                                            boardColumns[columnIndex].total = leadTotal
                                            boardColumns[columnIndex].items = leadComponents

                                            board.setAttr('columns', boardColumns)
                                        }
                                    })
                            }
                        })
                }""",

            # Load leads by status
            'loadLeads':
                """(app, params) => {
                    const { statusId, addToEnd=false } = params
                    const page = app.getView()
                    const board = page.getCom('leadsBoard')
                    const boardColumns = board.getAttr('columns')
                    const columnIndex = boardColumns.findIndex(c => c.key == statusId)

                    // Set loading to load button
                    boardColumns[columnIndex].loading = true
                    board.setAttr('columns', boardColumns)

                    app
                        .sendReq('getLeadComponents', {
                            statusId,
                            offset: addToEnd ? boardColumns[columnIndex].items.length : 0,
                            limit: addToEnd ? 10 : boardColumns[columnIndex].items.length,
                            search: '""" + str(params['search'] if params.get('search') else '') + """',
                            periodFrom: '""" + str(params['periodFrom'] if params.get('periodFrom') else '') + """',
                            periodTo: '""" + str(params['periodFrom'] if params.get('periodTo') else '') + """'
                        })
                        .then(result => {
                            // Unset loading to load button
                            boardColumns[columnIndex].loading = false
                            board.setAttr('columns', boardColumns)

                            if (result.res === 'ok') {
                                const { leadComponents, leadTotal, leadAmountSumStr } = result

                                // Set total and set/append items
                                boardColumns[columnIndex].total = leadTotal
                                boardColumns[columnIndex].subtitle = leadAmountSumStr
                                boardColumns[columnIndex].items = !addToEnd ? leadComponents : [
                                    ...boardColumns[columnIndex].items,
                                    ...leadComponents
                                ]

                                board.setAttr('columns', boardColumns)
                            }
                        })
                }""",

            # Drag lead between statuses
            'onDragLead':
                """(app, params, event) => {
                    const { key, oldColumnIndex, newColumnIndex, newColumnKey, oldItemIndex, newItemIndex } = event
                    const page = app.getView()
                    const board = page.getCom('leadsBoard')
                    const boardColumns = board.getAttr('columns')

                    // Get item from old column
                    const item = boardColumns[oldColumnIndex].items[oldItemIndex]
                    // Remove item from column
                    boardColumns[oldColumnIndex].items.splice(oldItemIndex, 1)
                    // Add item new column
                    boardColumns[newColumnIndex].items.splice(newItemIndex, 0, item)
                    // Sort by add date
                    boardColumns[newColumnIndex].items.sort((a, b) => a.order < b.order)

                    // Update columns on board
                    board.setAttr('columns', boardColumns)

                    app
                        .sendReq('updateLeadStatus', {
                            id: key,
                            statusId: +newColumnKey
                        })
                        .then(result => {
                            // Unset loading to both columns
                            app.getPage().callMethod('loadLeads', { statusId: boardColumns[oldColumnIndex].key })  
                            app.getPage().callMethod('loadLeads', { statusId: boardColumns[newColumnIndex].key })  
                        })
                }""",

            # On search
            'onSearchLeads': """(app, params, event) => {
                    app.getPage().to({
                        search: event.value,
                        periodFrom: '""" + str(params['periodFrom'] if params.get('periodFrom') else '') + """',
                        periodTo: '""" + str(params['periodFrom'] if params.get('periodTo') else '') + """'
                    })
                }""",

            # On change period
            'onChangePeriod': """(app, params, event) => {
                    app.getPage().to({ 
                        search: '""" + str(params['search'] if params.get('search') else '') + """',
                        periodFrom: event.value[0],
                        periodTo: event.value[1] 
                    })
                }"""
        }


# Get lead component
def get_lead_component(lead, installation_card_settings):
    title = ''
    description = []
    for field in lead['fields']:
        if field['value']:
            if field['field_board_visibility'] == 'title':
                title += field['value'] + ' '
            elif field['field_board_visibility'] == 'subtitle':
                description.append(field['value'])
    title = title.strip()

    extra = ['Archived' if lead['archived'] else Lead.get_regular_date(lead['add_date'])]
    if installation_card_settings.amount_enabled and lead['amount'] and lead['amount'] > 0:
        extra.insert(0, installation_card_settings.format_amount(lead['amount']))

    return {
        'key': lead['id'],
        'columnKey': lead['status_id'],
        'title': title if title else '#{}'.format(lead['uid']),
        'description': description if len(description) > 0 else None,
        'extra': extra,
        'order': lead['id'],
        'toWindow': ['updateLead', {
            'id': lead['id']
        }]
    }
