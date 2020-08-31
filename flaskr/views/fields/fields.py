from flaskr.views.view import View
from flaskr.models.field import Field, FieldType


# Page: Fields
class Fields(View):
    meta = {
        'name': 'Lead fields'
    }

    fields = []

    def before(self, params):
        self.fields = Field.query \
            .filter_by(veokit_system_id=1) \
            .all()

    def get_header(self, params):
        return {
            'title': self.meta.get('name'),
            'actions': [
                {
                    '_com': 'Button',
                    'label': 'Add field',
                    'type': 'primary',
                    'icon': 'plus',
                    'toWindow': 'createField'
                }
            ]
        }

    def get_schema(self, params):
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
            field_extra = []
            if field.as_title:
                field_extra.append('Show in title')
            if field.primary:
                field_extra.append({
                    '_com': 'Badge',
                    'dot': True,
                    'color': 'blue',
                    'text': 'Primary field'
                })

            list_items.append({
                'id': field.id,
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
                        'openModal': {
                            'title': 'Delete field',
                            'description': 'Are you sure you want to delete this field?',
                            'okText': 'Delete',
                            'onOk': ['deleteField', {
                                'id': field.id
                            }]
                        }
                    }
                ]
            })

        return [
            {
                '_com': 'List',
                'sortable': True,
                'onSort': 'onSortFields',
                'items': list_items
            }
        ]

    methods = {
        'onSortFields':
            """(app, params) => {
                
            }""",
        'deleteField':
            """(app, params) => {
                
            }"""
    }
