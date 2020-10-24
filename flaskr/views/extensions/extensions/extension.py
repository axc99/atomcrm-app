class Extension:
    def __init__(self):
        self.id = None
        self.key = None
        self.name = ''
        self.with_settings = False

    @staticmethod
    def get_default_data():
        return {}

    def get_schema_for_information(self, installation_extension_settings, params, request_data):
        return []

    def get_schema_for_settings(self, installation_extension_settings, params, request_data):
        return []

    def get_methods_for_settings(self, installation_extension_settings, params, request_data):
        return {}

    def webhook_process(self, params):
        return {}
