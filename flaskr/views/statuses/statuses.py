import enum
from flask_babel import _

from flaskr import db
from flaskr.views.view import View
from flaskr.models.status import Status, get_hex_by_color


# Page: Statuses
class Statuses(View):
    def __init__(self):
        self.meta = {
            'name': _('v_statuses_meta_name')
        }
        self.statuses = []

    def before(self, params, request_data):
        self.statuses = db.session.execute("""
            SELECT 
                s.*,
                (SELECT COUNT(*) FROM public.lead AS l WHERE l.status_id = s.id AND l.archived = false) AS lead_count,
                COUNT(*) OVER () AS total
            FROM 
                public.status AS s
            WHERE
                s.veokit_installation_id = :veokit_installation_id
            ORDER BY 
                s.index""", {
            'veokit_installation_id': request_data['installation_id']
        })

    def get_header(self, params, request_data):
        return {
            'title': self.meta.get('name'),
            'actions': [
                {
                    '_com': 'Button',
                    'label': _('v_statuses_header_createStatus'),
                    'type': 'primary',
                    'icon': 'plus',
                    'toWindow': 'createStatus'
                }
            ]
        }

    def get_schema(self, params, request_data):
        list_items = []

        for status in self.statuses:
            deleteButton = {
                '_com': 'Button',
                'icon': 'delete'
            }

            # If leads with this status exist
            if status.lead_count > 0:
                deleteButton['toWindow'] = ['deleteStatus', {
                    'id': status.id
                }]
            else:
                deleteButton['onClick'] = ['deleteStatus', {
                    'id': status.id
                }]

            list_items.append({
                'key': status.id,
                'color': get_hex_by_color(status.color),
                'title': status.name,
                'extra': "{} {}".format(status.lead_count, _('v_statuses_schema_count_lead') if status.lead_count == 1 else _('v_statuses_schema_count_leads')),
                'actions': [
                    {
                        '_com': 'Button',
                        'icon': 'edit',
                        'label': _('v_statuses_schema_editStatus'),
                        'toWindow': ['updateStatus', {
                            'id': status.id
                        }]
                    },
                    deleteButton
                ]
            })

        return [
            {
                '_com': 'List',
                '_id': 'statusesList',
                'draggable': True,
                'emptyText': _('v_statuses_schema_noStatuses'),
                'onDrag': 'onDragStatus',
                'items': list_items
            }
        ]

    methods = {
        'onDragStatus':
            """(app, params, event) => {
                const { key, newIndex, oldIndex } = event
                const window = app.getView()
                const list = window.getCom('statusesList')
                
                const items = list.getAttr('items')
                
                items.splice(newIndex, 0, items.splice(oldIndex, 1)[0])
                
                list.setAttr('items', items)
                
                app.sendReq('updateStatusIndex', {
                    id: key,
                    newIndex
                })
            }""",
        'deleteStatus':
            """(app, params) => {
                const { id } = params
                const window = app.getView()
                const list = window.getCom('statusesList')
                
                const items = list.getAttr('items')
                const item = items.find(item => item.key == id)
                
                // Set loading to delete button
                item.actions[1].loading = true
                list.setAttr('items', items)
                
                app
                    .sendReq('deleteStatus', {
                        id
                    })
                    .then(result => {
                        // Unset loading to delete button
                        item.actions[1].loading = false
                        list.setAttr('items', items)
                        
                        if (result.res == 'ok') {
                            // Reload parent page
                            app.getPage().reload()
                        }
                    })
            }"""
    }
