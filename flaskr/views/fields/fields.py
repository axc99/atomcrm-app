from flask_babel import _
from flaskr.views.view import View
from flaskr.models.field import Field, FieldType, get_field_types


# Page: Fields
class Fields(View):
    def __init__(self):
        self.meta = {
            'name': _('v_fields_meta_name')
        }
        self.fields = []

    def before(self, params, request_data):
        self.fields = Field.query \
            .filter_by(veokit_installation_id=request_data['installation_id']) \
            .order_by(Field.index.asc()) \
            .all()

    def get_header(self, params, request_data):
        return {
            'title': self.meta.get('name'),
            'actions': [
                {
                    '_com': 'Button',
                    'label': _('v_fields_header_createField'),
                    'type': 'primary',
                    'icon': 'plus',
                    'toWindow': 'createField'
                }
            ]
        }

    def get_schema(self, params, request_data):
        list_items = []
        field_types = get_field_types()

        for field in self.fields:
            field_description = next((t[2] for t in field_types if t[1] == field.value_type.name), None)

            # Extra with flags
            field_extra = {
                '_com': 'Tags',
                'items': []
            }
            if field.as_title:
                field_extra['items'].append({
                    'label': _('v_fields_schema_showInTitle')
                })
            if field.primary:
                field_extra['items'].append({
                    'label': _('v_fields_schema_primary')
                })

            list_items.append({
                'key': field.id,
                'title': field.name,
                'description': field_description,
                'extra': field_extra,
                'actions': [
                    {
                        '_com': 'Button',
                        'icon': 'edit',
                        'label': _('v_fields_schema_editField'),
                        'toWindow': ['updateField', {
                            'id': field.id
                        }]
                    },
                    {
                        '_com': 'Button',
                        'icon': 'delete',
                        'onClick': ['deleteField', {
                            'id': field.id
                        }]
                    }
                ]
            })

        return [
            {
                '_com': 'List',
                '_id': 'fieldsList',
                'draggable': True,
                'emptyText': _('v_fields_schema_noFields'),
                'onDrag': 'onDragFields',
                'items': list_items
            }
        ]

    methods = {
        'onDragFields':
            """(app, params, event) => {
                const { key, newIndex, oldIndex } = event
                const window = app.getView()
                const list = window.getCom('fieldsList')
                
                const items = list.getAttr('items')
                
                items.splice(newIndex, 0, items.splice(oldIndex, 1)[0])
                
                list.setAttr('items', items)
                
                app.sendReq('updateFieldIndex', {
                    id: key,
                    newIndex
                })
            }""",
        'deleteField':
            """(app, params) => {
                const { id } = params
                const window = app.getView()
                const list = window.getCom('fieldsList')
                
                const items = list.getAttr('items')
                const item = items.find(item => item.key == id)
                
                item.actions[1].loading = true
                list.setAttr('items', items)
                
                app
                    .sendReq('deleteField', { id })
                    .then(result => {
                        item.actions[1].loading = false
                        list.setAttr('items', items)
                        
                        if (result.res == 'ok') {
                            // Reload parent page
                            app.getPage().reload()
                        }
                    })
            }"""
    }
