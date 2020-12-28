class Extension:
    id = None
    key = None
    name = ''
    with_settings = False

    @staticmethod
    def get_default_data():
        return {}

    @staticmethod
    def catch_webhook(installation_extension_settings, webhook_key=None):
        return 'OK'

    def get_scheme_for_information(self, installation_extension_settings, params, request_data):
        return []

    def get_scheme_for_settings(self, installation_extension_settings, params, request_data):
        return []

    def get_data_for_settings(self, installation_extension_settings, params, request_data):
        return []

    def get_script_for_settings(self, installation_extension_settings, params, request_data):
        return None

    def get_methods_for_settings(self, installation_extension_settings, params, request_data):
        return {}
