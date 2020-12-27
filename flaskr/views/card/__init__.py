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
                'scheme_form_leadAmount': _('v_card_scheme_form_leadAmount'),
                'scheme_form_amountCurrency': _('v_card_scheme_form_amountCurrency'),
                'scheme_form_fields': _('v_card_scheme_form_fields'),
                'scheme_form_fields_table_noFields': _('v_card_scheme_form_fields_table_noFields'),
                'scheme_form_fields_table_field': _('v_card_scheme_form_fields_table_field'),
                'scheme_form_fields_table_valueType': _('v_card_scheme_form_fields_table_valueType'),
                'scheme_form_fields_table_boardVisibility': _('v_card_scheme_form_fields_table_boardVisibility'),
                'scheme_form_fields_addField': _('v_card_scheme_form_fields_addField'),
                'scheme_form_save': _('v_card_scheme_form_save'),
                'schema_form_fields_table_none': 'None',
                'schema_form_fields_table_title': 'Title',
                'schema_form_fields_table_subtitle': 'Subtitle',
                'changesSaved': _('v_card_getMethods_changesSaved')
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
