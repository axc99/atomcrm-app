from flask_babel import _
from flaskr.views.view import View, get_method, method_with_vars, compile_js
from flaskr.models.field import Field, FieldType, get_field_types, get_board_visibility
from flaskr.models.installation_card_settings import InstallationCardSettings
from flaskr.data.currencies import currencies

script = compile_js('script')


# Page: Card (Information + Fields)
class Card(View):
    def __init__(self):
        self.script = script
        self.meta = {
            'name': _('v_card_meta_name')
        }
        self.data = {
            'currencies': [],
            'strs': {
                'name': _('v_card_meta_name'),
                'form_leadAmount': _('v_card_form_leadAmount'),
                'form_amountCurrency': _('v_card_form_amountCurrency'),
                'form_fields': _('v_card_form_fields'),
                'form_fields_table_noFields': _('v_card_form_fields_table_noFields'),
                'form_fields_table_field': _('v_card_form_fields_table_field'),
                'form_fields_table_valueType': _('v_card_form_fields_table_valueType'),
                'form_fields_table_valueType_string': _('v_card_form_fields_table_valueType_string'),
                'form_fields_table_valueType_email': _('v_card_form_fields_table_valueType_email'),
                'form_fields_table_valueType_phone': _('v_card_form_fields_table_valueType_phone'),
                'form_fields_table_valueType_longString': _('v_card_form_fields_table_valueType_longString'),
                'form_fields_table_valueType_number': _('v_card_form_fields_table_valueType_number'),
                'form_fields_table_valueType_boolean': _('v_card_form_fields_table_valueType_boolean'),
                'form_fields_table_valueType_date': _('v_card_form_fields_table_valueType_date'),
                'form_fields_table_valueType_choice': _('v_card_form_fields_table_valueType_choice'),
                'form_fields_table_boardVisibility': _('v_card_form_fields_table_boardVisibility'),
                'form_fields_table_boardVisibility_none': _('v_card_form_fields_table_boardVisibility_none'),
                'form_fields_table_boardVisibility_title': _('v_card_form_fields_table_boardVisibility_title'),
                'form_fields_table_boardVisibility_subtitle': _('v_card_form_fields_table_boardVisibility_subtitle'),
                'form_fields_addField': _('v_card_form_fields_addField'),
                'form_save': _('v_card_form_save'),
                'form_fields_table_none': 'None',
                'form_fields_table_title': 'Title',
                'form_fields_table_subtitle': 'Subtitle',
                'notification_changesSaved': _('v_card_getMethods_changesSaved')
            }
        }
        self.installation_card_settings = None
        self.fields = []
        self.value_type_options = []
        self.board_visibility_options = []

    def before(self, params, request_data):
        installation_card_settings = InstallationCardSettings.query \
            .filter_by(nepkit_installation_id=request_data['installation_id']) \
            .first()

        # Currency select
        currencies_to_data = []
        for key, currency in currencies.items():
            currencies_to_data.append({
                'key': key,
                'namePlural': currency['name_plural'],
                'code': currency['code']
            })

        self.data['installationCardSettings'] = {
            'amountEnabled': installation_card_settings.amount_enabled,
            'currency': installation_card_settings.currency.name
        }
        self.data['currencies'] = currencies_to_data
