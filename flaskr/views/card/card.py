from flask_babel import _
from flaskr.views.view import View
from flaskr.models.field import Field, FieldType, get_field_types, get_board_visibility
from flaskr.models.installation_card_settings import InstallationCardSettings
from flaskr.data.currencies import currencies


# Page: Card (Information + Fields)
class Card(View):
    def __init__(self):
        self.meta = {
            'name': _('v_card_meta_name')
        }
        self.installation_card_settings = None
        self.fields = []
        self.value_type_options = []
        self.currency_options = []
        self.board_visibility_options = []

    def before(self, params, request_data):
        self.installation_card_settings = InstallationCardSettings.query \
            .filter_by(veokit_installation_id=request_data['installation_id']) \
            .first()
        self.fields = Field.query \
            .filter_by(veokit_installation_id=request_data['installation_id']) \
            .order_by(Field.index.asc()) \
            .all()

        # Value type select
        for t in get_field_types():
            if t[1] not in ('boolean', 'select',):
                self.value_type_options.append({'value': t[1], 'label': t[2]})

        # Currency select
        for key, currency in currencies.items():
            self.currency_options.append({
                'value': key,
                'label': "{} - {}".format(currency['code'], currency['name_plural'])
            })

        # Board visibility
        for v in get_board_visibility():
            self.board_visibility_options.append({
                'value': v[1],
                'label': v[2]
            })

    def get_header(self, params, request_data):
        return {
            'title': self.meta.get('name')
        }

    def get_schema(self, params, request_data):
        table_rows = []
        for field in self.fields:
            table_rows.append({
                'key': field.id,
                'name': {
                    '_com': 'Field.Input',
                    'value': field.name
                },
                'valueType': {
                    '_com': 'Field.Select',
                    'options': self.value_type_options,
                    'value': field.value_type.name
                },
                'boardVisibility': {
                    '_com': 'Field.Select',
                    'options': self.board_visibility_options,
                    'value': field.board_visibility.name
                },
                'actions': [
                    {
                        '_com': 'Button',
                        'icon': 'delete',
                        'onClick': ['onClickDeleteField', {
                            'index': field.index
                        }]
                    }
                ]
            })

        return [
            {
                '_com': 'Form',
                '_id': 'updateCardSettingsForm',
                'onFinish': 'onFinish',
                'fields': [
                    {
                        '_com': 'Field.Checkbox',
                        'key': 'amountEnabled',
                        'text': _('v_card_scheme_form_leadAmount'),
                        'value': self.installation_card_settings.amount_enabled,
                        'onChange': 'onChangeAmountEnabled'
                    },
                    {
                        '_com': 'Field.Select',
                        'key': 'currency',
                        'withSearch': True,
                        'disabled': not self.installation_card_settings.amount_enabled,
                        'label': _('v_card_scheme_form_amountCurrency'),
                        'value': self.installation_card_settings.currency.name,
                        'options': self.currency_options
                    },
                    {
                        '_com': 'Field.Custom',
                        '_id': 'updateCardSettingsForm_fields',
                        'columnWidth': 10,
                        'label': _('v_card_scheme_form_fields'),
                        'content': [
                            {
                                '_com': 'Table',
                                '_id': 'updateCardSettingsForm_fields_table',
                                'draggable': True,
                                'emptyText': _('v_card_scheme_form_fields_table_noFields'),
                                'onDrag': 'onDragFields',
                                'columns': [
                                    {
                                        'width': 35,
                                        'key': 'name',
                                        'title': _('v_card_scheme_form_fields_table_field')
                                    },
                                    {
                                        'width': 35,
                                        'key': 'valueType',
                                        'title': _('v_card_scheme_form_fields_table_valueType')
                                    },
                                    {
                                        'width': 30,
                                        'key': 'boardVisibility',
                                        'title': _('v_card_scheme_form_fields_table_boardVisibility')
                                    }
                                ],
                                'rows': table_rows
                            },
                            {
                                '_com': 'Button',
                                '_id': 'updateCardSettingsForm_fields_addBtn',
                                'label': _('v_card_scheme_form_fields_addField'),
                                'icon': 'plus',
                                'type': 'solid',
                                'onClick': 'onClickAddField'
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
                        'label': _('v_card_scheme_form_save')
                    }
                ]
            }
        ]

    def get_methods(self, params, request_data):
        return {
            'onDragFields':
                """(app, params, event) => {
                    const window = app.getView()
                    const fieldsTable = window.getCom('updateCardSettingsForm_fields_table')
                    const rows = fieldsTable.getAttr('rows')
                    const { oldIndex, newIndex } = event

                    rows.splice(newIndex, 0, rows.splice(oldIndex, 1)[0])

                    fieldsTable.setAttr('rows', rows)
                }""",
            'onClickAddField':
                """(app, params, event) => {
                    const window = app.getView()
                    const fieldsTable = window.getCom('updateCardSettingsForm_fields_table')
                    const rows = fieldsTable.getAttr('rows')

                    rows.push({
                        'name': {
                            '_com': 'Field.Input'
                        },
                        'valueType': {
                            '_com': 'Field.Select',
                            'options': """ + str(self.value_type_options) + """,
                            'value': 'string'
                        },
                        boardVisibility: {
                            '_com': 'Field.Select',
                            'value': 'subtitle',
                            'options': [
                                {'value': 'none', 'label': 'Do not show'},
                                {'value': 'title', 'label': 'Show in title'},
                                {'value': 'subtitle', 'label': 'Show in description'}
                            ]
                        },
                        actions: [
                            {
                                '_com': 'Button',
                                'icon': 'delete',
                                'onClick': ['onClickDeleteField', {
                                    'index': rows.length
                                }]
                            }
                        ]
                    })

                    fieldsTable.setAttr('rows', rows)
                }""",
            'onClickDeleteField':
                """(app, params, event) => {
                    const window = app.getView()
                    const fieldsTable = window.getCom('updateCardSettingsForm_fields_table')
                    let rows = fieldsTable.getAttr('rows')
                    delete rows[params.index]
                    fieldsTable.setAttr('rows', rows)
                }""",
            'onChangeAmountEnabled':
                """(app, params, event) => {
                    const { value } = event
                    const page = app.getPage()
                    const form = page.getCom('updateCardSettingsForm')
                    const fields = form.getAttr('fields')
                    
                    const currencyField = fields.find(f => f.key == 'currency')
                    currencyField.disabled = !value
                    
                    form.setAttr('fields', fields)
                }""",
            'onFinish':
                """(app, params, event) => {
                    const { values } = event
                    const page = app.getPage()
                    const form = page.getCom('updateCardSettingsForm')
                    const fieldsTable = page.getCom('updateCardSettingsForm_fields_table')
                    const rows = fieldsTable.getAttr('rows')

                    form.setAttr('loading', true)

                    const fields = []
                    rows.map(row => {
                        fields.push({
                            id: row.key,
                            name: row.name.value,
                            valueType: row.valueType.value,
                            boardVisibility: row.boardVisibility.value
                        })
                    })

                    app
                        .sendReq('updateCardSettings', {
                            amountEnabled: values.amountEnabled,
                            currency: values.currency,
                            fields
                        })
                        .then(result => {
                            form.setAttr('loading', false)

                            if (result.res == 'ok') {
                                app
                                    .getPage()
                                    .to('pipeline')
                            }
                        })
                }"""
        }