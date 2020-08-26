class View:
    def __init__(self):
        self.header = {}
        self.schema = []
        self.methods = {}

    def get_methods(self):
        return self.methods

    def get_header(self):
        return self.header

    def get_schema(self):
        return self.schema
