from flaskr.views.view import View
from flaskr.models.field import Field, FieldType


# Page: Fields
class Fields(View):
    meta = {
        'name': 'Lead fields'
    }

    fields = []

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
                    'label': 'Create field',
                    'type': 'primary',
                    'icon': 'plus',
                    'toWindow': 'createField'
                }
            ]
        }

    def get_schema(self, params, request_data):
        list_items = []

        for field in self.fields:

            # Description with field type, min and max values
            field_description = ''
            if field.value_type == FieldType.string:
                field_description = 'String ({} - {} length)'.format(field.min, field.max)
            elif field.value_type == FieldType.number:
                field_description = 'Number ({} - {})'.format(field.min, field.max)
            elif field.value_type == FieldType.boolean:
                field_description = 'Checkbox'
            elif field.value_type == FieldType.select:
                field_description = 'Dropdown select ({} options)'.format(23)

            # Extra with flags
            field_extra = {
                '_com': 'Tags',
                'items': []
            }
            if field.as_title:
                field_extra['items'].append({
                    'label': 'Show in title'
                })
            if field.primary:
                field_extra['items'].append({
                    'label': 'Primary field'
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
                        'label': 'Edit field',
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
                'sortable': True,
                'emptyText': 'No fields',
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
                    newIndex,
                    oldIndex
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
                        
                        if (result._res == 'ok') {
                            // Reload parent page
                            app.getPage().reload()
                        }
                    })
            }"""
    }
