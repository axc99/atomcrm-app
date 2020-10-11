from flask_babel import _
from flaskr.views.view import View
from flaskr.models.field import get_field_types


# Window: Create Field
class CreateField(View):
    def __init__(self):
        self.meta = {
            'name': _('v_createField_meta_name')
        }

    def get_header(self, params, request_data):
        return {
            'title': self.meta.get('name')
        }

    def get_schema(self, params, request_data):
        field_types = get_field_types()
        value_type_options = []
        for t in field_types:
            value_type_options.append({'value': t[1], 'label': t[2]})

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
                        'label': _('v_createField_form_name'),
                        'placeholder': _('v_createField_form_name_placeholder'),
                        'maxLength': 20,
                        'rules': [
                            {'min': 2, 'max': 20, 'message': _('v_createField_form_name_length')},
                            {'required': True, 'message': _('v_createField_form_name_required')}
                        ]
                    },
                    {
                        '_com': 'Field.Select',
                        'value': 'string',
                        'key': 'valueType',
                        'label': _('v_createField_form_valueType'),
                        'options': value_type_options,
                        'rules': [
                            {'required': True, 'message': _('v_createField_form_valueType_required')}
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
                        'label': _('v_createField_form_minLength'),
                        'rules': [
                            {'required': True, 'message': _('v_createField_form_minLength_required')}
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
                        'label': _('v_createField_form_maxLength'),
                        'rules': [
                            {'required': True, 'message': _('v_createField_form_maxLength_required')}
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
                        'label': _('v_createField_form_min'),
                        'rules': [
                            {'required': True, 'message': _('v_createField_form_min_required')}
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
                        'label': _('v_createField_form_max'),
                        'rules': [
                            {'required': True, 'message': _('v_createField_form_max_required')}
                        ]
                    },
                    {
                        '_com': 'Field.CheckboxGroup',
                        'key': 'flags',
                        'items': [
                            {
                                'key': 'asTitle',
                                'label': _('v_createField_form_fieldAsTitle')
                            },
                            {
                                'key': 'primary',
                                'label': _('v_createField_form_primaryField')
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
                        'label': _('v_createField_form_create')  # 'Create'
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
                        min: values.valueType === 'number' ? +values.min : +values.minLength,
                        max: values.valueType === 'number' ? +values.max : +values.maxLength,
                        asTitle: !!(values.flags && values.flags.includes('asTitle')),
                        primary: !!(values.flags && values.flags.includes('primary'))
                    })
                    .then(result => {
                        form.setAttr('loading', false)
                        
                        if (result.res == 'ok') {
                            // Reload parent page
                            app.getPage().reload()
                        }
                    })
            }"""
    }
