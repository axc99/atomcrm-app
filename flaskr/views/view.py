class View:
    meta = {}
    header = {}
    schema = []
    methods = {}

    def before(self, params, request_data):
        pass

    def before_get_meta(self, params, request_data):
        pass

    def before_get_methods(self, params, request_data):
        pass

    def before_get_header(self, params, request_data):
        pass

    def before_get_schema(self, params, request_data):
        pass

    def get_meta(self, params, request_data):
        return self.meta

    def get_methods(self, params, request_data):
        return self.methods

    def get_header(self, params, request_data):
        return self.header

    def get_schema(self, params, request_data):
        return self.schema
