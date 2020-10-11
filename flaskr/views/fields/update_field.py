from flask_babel import _
from cerberus import Validator

from flaskr.views.view import View
from flaskr.models.field import Field, get_field_types


# Window: Update field
class UpdateField(View):
    def __init__(self):
        self.meta = {
            'name': _('v_updateField_meta_name')
        }
        self.field = None

    def before(self, params, request_data):
        vld = Validator({
            'id': {'type': 'number', 'required': True}
        })
        is_valid = vld.validate(params)
        if not is_valid:
            raise Exception({'message': 'Invalid params',
                             'errors': vld.errors})

        self.field = Field.query \
            .filter_by(id=params['id'],
                       veokit_installation_id=request_data['installation_id']) \
            .first()
        if not self.field:
            raise Exception()

    def get_header(self, params, request_data):
        return {
            'title': self.meta.get('name')
        }

    def get_schema(self, params, request_data):
        field_types = get_field_types()
        value_type_options = []
        for t in field_types:
            value_type_options.append({'value': t[1], 'label': t[2]})

        length_fields_vis = self.field.value_type.name in ('string', 'long_string')
        num_fields_vis = self.field.value_type.name == 'number'

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
                        'label': _('v_updateField_form_name'),
                        'placeholder': _('v_updateField_form_placeholder'),
                        'maxLength': 20,
                        'value': self.field.name,
                        'rules': [
                            {'min': 2, 'max': 20, 'message': _('v_updateField_form_name_length')},
                            {'required': True, 'message': _('v_updateField_form_name_required')}
                        ]
                    },
                    {
                        '_com': 'Field.Select',
                        'value': self.field.value_type.name,
                        'key': 'valueType',
                        'label': _('v_updateField_form_valueType'),
                        'options': value_type_options,
                        'rules': [
                            {'required': True, 'message': _('v_updateField_form_valueType_required')}
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
                        'label': _('v_updateField_form_minLength'),
                        'rules': [
                            {'required': True, 'message': _('v_updateField_form_minLength_required')}
                        ]
                    },
                    {
                        '_com': 'Field.Input',
                        '_id': 'createFieldForm_maxLength',
                        '_vis': length_fields_vis,
                        'type': 'number',
                        'columnWidth': 6,
                        'value': self.field.max,
                        'max': 500,
                        'key': 'maxLength',
                        'label': _('v_updateField_form_maxLength'),
                        'rules': [
                            {'required': True, 'message': _('v_updateField_form_maxLength_required')}
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
                        'label': _('v_updateField_form_min'),
                        'rules': [
                            {'required': True, 'message': _('v_updateField_form_min_required')}
                        ]
                    },
                    {
                        '_com': 'Field.Input',
                        '_vis': num_fields_vis,
                        '_id': 'createFieldForm_max',
                        'type': 'number',
                        'columnWidth': 6,
                        'value': self.field.max,
                        'max': 2147483647,
                        'key': 'max',
                        'label': _('v_updateField_form_max'),
                        'rules': [
                            {'required': True, 'message': _('v_updateField_form_max_required')}
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
                                'label': _('v_updateField_form_fieldAsTitle')
                            },
                            {
                                'key': 'primary',
                                'label': _('v_updateField_form_primaryField')
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
                        'label': _('v_updateField_form_save')
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
