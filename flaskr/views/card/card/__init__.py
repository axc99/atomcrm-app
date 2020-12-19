from flask_babel import _
from flaskr.views.view import View, get_method, method_with_vars
from flaskr.models.field import Field, FieldType, get_field_types, get_board_visibility
from flaskr.models.installation_card_settings import InstallationCardSettings
from flaskr.data.currencies import currencies

compiled_methods = {
    'onChangeValueType': get_method('methods/onChangeValueType'),
    'onDragFields': get_method('methods/onDragFields'),
    'onClickAddField': get_method('methods/onClickAddField'),
    'onClickDeleteField': get_method('methods/onClickDeleteField'),
    'onChangeAmountEnabled': get_method('methods/onChangeAmountEnabled'),
    'onFinishForm': get_method('methods/onFinishForm')
}


def json_options_to_text(json):
    lines = []

    if json:
        for field_key, field_value in json.items():
            lines.append("{}={}".format(field_key, field_value))

    return '\r'.join(lines)


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
            .filter_by(nepkit_installation_id=request_data['installation_id']) \
            .first()
        self.fields = Field.query \
            .filter_by(nepkit_installation_id=request_data['installation_id']) \
            .order_by(Field.index.asc()) \
            .all()

        # Value type select
        for t in get_field_types():
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
        i = 0
        for field in self.fields:
            table_rows.append({
                'key': field.id,
                'name': {
                    '_com': 'Field.Input',
                    'value': field.name,
                    'maxLength': 40
                },
                'valueType': [
                    {
                        '_com': 'Field.Select',
                        'onChange': ['onChangeValueType', {'fieldIndex': i}],
                        'options': self.value_type_options,
                        'value': field.value_type.name
                    },
                    {
                        '_com': 'Field.Input',
                        'multiline': True,
                        'maxLength': 500,
                        'placeholder': 'key=value',
                        'value': json_options_to_text(field.choice_options)
                    } if field.value_type.name == 'choice' else None
                ],
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
            i += 1

        return [
            {
                '_com': 'Form',
                '_id': 'updateCardSettingsForm',
                'onFinish': 'onFinishForm',
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
                        'columnWidth': 12,
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
        methods = compiled_methods.copy()

        methods['onClickAddField'] = method_with_vars(methods['onClickAddField'], {'VALUE_TYPE_OPTIONS': self.value_type_options,
                                                                                   'BOARD_VISIBILITY_OPTIONS': self.board_visibility_options})
        methods['onFinishForm'] = method_with_vars(methods['onFinishForm'],
                                                      {'SAVING_NOTIFICATION_MESSAGE': _('v_card_getMethods_changesSaved')})

        return methods
