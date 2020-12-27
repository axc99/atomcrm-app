from flask_babel import _

from cerberus import Validator
from flaskr.models.installation_extension_settings import InstallationExtensionSettings
from flaskr.extensions import extensions_map
from flaskr.views.view import View, get_method

compiled_methods = {
    'onFinishForm': get_method('methods/onFinishForm')
}


# Page: Extension
class Extension(View):
    def __init__(self):
        self.meta = {}
        self.tab = 'information'
        self.extension = None
        self.installation_extension_settings = None

    def before(self, params, request_data):
        vld = Validator({
            'key': {'type': 'string', 'required': True},
            'tab': {'type': 'string', 'nullable': True}
        })
        is_valid = vld.validate(params)
        if not is_valid:
            raise Exception({'message': 'Invalid params',
                             'errors': vld.errors})

        nepkit_extension_id = extensions_map[params['key']].id

        self.installation_extension_settings = InstallationExtensionSettings.query \
            .filter_by(nepkit_extension_id=nepkit_extension_id,
                       nepkit_installation_id=request_data['installation_id']) \
            .first()

        self.tab = params['tab'] if params.get('tab') else 'information'
        self.extension = extensions_map[params['key']]()
        self.meta = {
            'name': _('v_extension_meta_name', name=self.extension.name)
        }

        if self.tab == 'settings':
            self.data = self.extension.get_data_for_settings(self.installation_extension_settings, params, request_data)
            self.script = self.extension.get_script_for_settings(self.installation_extension_settings, params, request_data)

    def get_header(self, params, request_data):
        print('self.extension', self.extension.with_settings)
        return {
            'title': self.meta['name'],
            'breadcrumb': [
                {
                    'text': _('v_extension_header_tab_extensions'),
                    'to': ['control', {'tab': 'extensions'}]
                },
                {
                    'text': self.extension.name
                }
            ],
            'tabs': [
                {
                    'text': _('v_extension_header_information'),
                    'to': ['extension', {'key': params['key']}],
                    'key': 'information'
                },
                {
                    'text': _('v_extension_header_settings'),
                    'to': ['extension', {'key': params['key'], 'tab': 'settings'}],
                    'key': 'settings'
                }
            ] if self.extension.with_settings else None,
            'activeTab': self.tab
        }

    def get_schema(self, params, request_data):
        if self.tab == 'information':
            return self.extension.get_schema_for_information(self.installation_extension_settings, params, request_data)
        elif self.tab == 'settings':
            return self.extension.get_schema_for_settings(self.installation_extension_settings, params, request_data)

    def get_methods(self, params, request_data):
        if self.tab == 'settings':
            return self.extension.get_methods_for_settings(self.installation_extension_settings, params, request_data)

    methods = compiled_methods