import enum
from flask_babel import _
import os

from cerberus import Validator
from flaskr import db
from flaskr.models.installation_extension_settings import InstallationExtensionSettings
from flaskr.views.extensions.extensions import extensions_map
from flaskr.views.view import View


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

        veokit_extension_id = extensions_map[params['key']].id

        self.installation_extension_settings = InstallationExtensionSettings.query \
            .filter_by(veokit_extension_id=veokit_extension_id,
                       veokit_installation_id=request_data['installation_id']) \
            .first()

        self.tab = params['tab'] if params.get('tab') else 'information'
        self.extension = extensions_map[params['key']]()
        self.meta = {
            'name': _('v_extension_meta_name', name=self.extension.name)
        }

    def get_header(self, params, request_data):
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
            ],
            'activeTab': self.tab
        }

    def get_schema(self, params, request_data):
        if self.tab == 'information':
            return self.get_schema_for_information(params, request_data)
        elif self.tab == 'settings':
            return self.get_schema_for_settings(params, request_data)

    def get_schema_for_information(self, params, request_data):
        return self.extension.get_schema_for_information(self.installation_extension_settings, params, request_data)

    def get_schema_for_settings(self, params, request_data):
        return self.extension.get_schema_for_settings(self.installation_extension_settings, params, request_data)

    def get_methods(self, params, request_data):
        return self.extension.get_methods_for_settings(self.installation_extension_settings, params, request_data)
