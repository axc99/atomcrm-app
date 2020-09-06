from flaskr.views.view import View


# Window: Create Field
class CreateField(View):
    meta = {
        'name': 'Create field'
    }

    def get_header(self, params, request_data):
        return {
            'title': self.meta.get('name')
        }

    def get_schema(self, params, request_data):
        value_type_options = [
            {'value': 'string', 'label': 'Text'},
            {'value': 'long_string', 'label': 'Long text'},
            {'value': 'number', 'label': 'Number'},
            {'value': 'boolean', 'label': 'Checkbox'},
            # {'value': 'select', 'label': 'Select list'}
        ]

        return [
            {
                '_com': 'Form',
                '_id': 'createFieldForm',
                'onFinish': 'onFinish',
                'fields': [
                    {
                        '_com': 'Field.Input',
                        'type': 'text',
                        'key': 'name',
                        'label': 'Field name',
                        'placeholder': 'Ex: Promocode',
                        'maxLength': 20,
                        'rules': [
                            {'min': 2, 'max': 20, 'message': 'Must contain 2 - 20 chars'},
                            {'required': True, 'message': 'Name is required'}
                        ]
                    },
                    {
                        '_com': 'Field.Select',
                        'value': 'string',
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
                        'type': 'number',
                        'columnWidth': 6,
                        'value': '0',
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
                        'type': 'number',
                        'columnWidth': 6,
                        'value': '100',
                        'max': 500,
                        'key': 'maxLength',
                        'label': 'Max length',
                        'rules': [
                            {'required': True, 'message': 'Max length is required'}
                        ]
                    },
                    {
                        '_com': 'Field.Input',
                        '_vis': False,
                        '_id': 'createFieldForm_min',
                        'type': 'number',
                        'columnWidth': 6,
                        'value': '0',
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
                        'value': '100',
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
                        'icon': 'plus',
                        'label': 'Create'
                    }
                ]
            }
        ]

    methods = {
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
                const form = window.getCom('createFieldForm')
                const { values } = event
                
                form.setAttr('loading', true)
                
                app
                    .sendReq('createField', {
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
