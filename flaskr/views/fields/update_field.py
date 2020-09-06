from flaskr.views.view import View
from flaskr.models.field import Field


# Window: Update field
class UpdateField(View):
    field = None

    def before(self, params, request_data):
        id = params.get('id')

        if not id:
            raise Exception()

        self.field = Field.query \
            .filter_by(id=id,
                       veokit_installation_id=request_data['installation_id']) \
            .first()
        if not self.field:
            raise Exception()

    def get_header(self, params, request_data):
        return {
            'title': 'Edit field'
        }

    def get_schema(self, params, request_data):
        value_type_options = [
            {'value': 'string', 'label': 'Text'},
            {'value': 'long_string', 'label': 'Long text'},
            {'value': 'number', 'label': 'Number'},
            {'value': 'boolean', 'label': 'Checkbox'},
            # {'value': 'select', 'label': 'Select list'}
        ]

        length_fields_vis = self.field.value_type in ['string', 'long_string']
        num_fields_vis = self.field.value_type == 'number'

        return [
            {
                '_com': 'Form',
                '_id': 'updateFieldForm',
                'onFinish': 'onFinish',
                'fields': [
                    {
                        '_com': 'Field.Input',
                        'type': 'text',
                        'key': 'name',
                        'label': 'Field name',
                        'placeholder': 'Ex: Promocode',
                        'maxLength': 20,
                        'value': self.field.name,
                        'rules': [
                            {'min': 2, 'max': 20, 'message': 'Must contain 2 - 20 chars'},
                            {'required': True, 'message': 'Name is required'}
                        ]
                    },
                    {
                        '_com': 'Field.Select',
                        'value': self.field.value_type.name,
                        'key': 'valueType',
                        'label': 'Value type',
                        'options': value_type_options,
                        'rules': [
                            {'required': True, 'message': 'Value type is required'}
                        ],
                        'onChange': 'onChangeValueType'
                    },
                    {
                        '_com': 'Field.Input',
                        '_id': 'createFieldForm_minLength',
                        '_vis': length_fields_vis,
                        'type': 'number',
                        'columnWidth': 6,
                        'value': self.field.min,
                        'min': 0,
                        'key': 'minLength',
                        'label': 'Min length',
                        'rules': [
                            {'required': True, 'message': 'Min length is required'}
                        ]
                    },
                    {
                        '_com': 'Field.Input',
                        '_id': 'createFieldForm_maxLength',
                        '_vis': num_fields_vis,
                        'type': 'number',
                        'columnWidth': 6,
                        'value': self.field.max,
                        'max': 500,
                        'key': 'maxLength',
                        'label': 'Max length',
                        'rules': [
                            {'required': True, 'message': 'Max length is required'}
                        ]
                    },
                    {
                        '_com': 'Field.Input',
                        '_id': 'createFieldForm_min',
                        '_vis': num_fields_vis,
                        'type': 'number',
                        'columnWidth': 6,
                        'value': self.field.min,
                        'min': 0,
                        'key': 'min',
                        'label': 'Min',
                        'rules': [
                            {'required': True, 'message': 'Min is required'}
                        ]
                    },
                    {
                        '_com': 'Field.Input',
                        '_vis': False,
                        '_id': 'createFieldForm_max',
                        'type': 'number',
                        'columnWidth': 6,
                        'value': self.field.max,
                        'max': 2147483647,
                        'key': 'max',
                        'label': 'Max',
                        'rules': [
                            {'required': True, 'message': 'Max is required'}
                        ]
                    },
                    {
                        '_com': 'Field.CheckboxGroup',
                        'key': 'flags',
                        'value': [
                            'asTitle' if self.field.as_title else None,
                            'primary' if self.field.primary else None
                        ],
                        'items': [
                            {
                                'key': 'asTitle',
                                'label': 'Field as title'
                            },
                            {
                                'key': 'primary',
                                'label': 'Primary field'
                            }
                        ]
                    }
                ],
                'buttons': [
                    {
                        '_com': 'Button',
                        'type': 'primary',
                        'submitForm': True,
                        'icon': 'save',
                        'label': 'Save'
                    }
                ]
            }
        ]

    def get_methods(self, params, request_data):
        return {
            'onChangeValueType':
                """(app, params, event) => {
                    const { value } = event
                    const window = app.getView()
                    const minLengthField = window.getCom('createFieldForm_minLength')
                    const maxLengthField = window.getCom('createFieldForm_maxLength')
                    const minField = window.getCom('createFieldForm_min')
                    const maxField = window.getCom('createFieldForm_max')

                    const lengthFieldsVis = ['string', 'long_string'].includes(value)
                    const numFieldsVis = value == 'number'

                    if (lengthFieldsVis) {
                        minLengthField.show()
                        maxLengthField.show()
                    } else {
                        minLengthField.hide()
                        maxLengthField.hide()
                    }

                    if (numFieldsVis) {
                        minField.show()
                        maxField.show()
                    } else {
                        minField.hide()
                        maxField.hide()
                    }
                }""",
            'onFinish':
                """(app, params, event) => {
                    const window = app.getView()
                    const form = window.getCom('updateFieldForm')
                    const { values } = event

                    form.setAttr('loading', true)

                    app
                        .sendReq('updateField', {
                            id: """ + str(self.field.id) + """,
                            name: values.name,
                            valueType: values.valueType,
                            min: values.valueType === 'number' ? values.min : values.minLength,
                            max: values.valueType === 'number' ? values.max : values.maxLength,
                            asTitle: values.flags && values.flags.includes('asTitle'),
                            primary: values.flags && values.flags.includes('primary')
                        })
                        .then(result => {
                            form.setAttr('loading', false)

                            if (result._res == 'ok') {
                                // Reload parent page
                                app.getPage().reload()
                            }
                        })
                }"""
        }
