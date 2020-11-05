import os
import traceback
import dukpy


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


# Compile ES6/ES7 method to ES5
def get_method(location):
    stack = traceback.extract_stack()
    dir = os.path.dirname(os.path.realpath(stack[-2].filename))

    filename = os.path.join(dir, "{}.js".format(location))
    prod_filename = os.path.join(dir, "{}.prod.js".format(location))

    if os.environ.get('FLASK_ENV') == 'production' and os.path.isfile(prod_filename):
        file = open(prod_filename, 'r')
    else:
        file = open(filename, 'r')

    code = file.read()
    file.close()

    return code


# Interpolate VAR into compile js function
def method_with_vars(code, vars):
    for key in vars:
        code = code.replace(key, str(vars[key]))

    return code
