class View:
    meta = {}
    header = {}
    schema = []
    methods = {}

    def before(self, params):
        pass

    def before_get_meta(self, params):
        pass

    def before_get_methods(self, params):
        pass

    def before_get_header(self, params):
        pass

    def before_get_schema(self, params):
        pass

    def get_meta(self, params):
        return self.meta

    def get_methods(self, params):
        return self.methods

    def get_header(self, params):
        return self.header

    def get_schema(self, params):
        return self.schema
