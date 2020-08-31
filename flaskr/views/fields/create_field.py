from flaskr.views.view import View


# Window: Create Field
class CreateField(View):
    meta = {
        'name': 'Create field'
    }

    def get_header(self, params):
        return {
            'title': self.meta.get('name')
        }

    def get_schema(self, params):
        return [
            {
                '_com': 'Form',
                'onSubmit': 'onSubmitForm',
                'fields': [],
                'buttons': [
                    {
                        '_com': 'Button',
                        'type': 'primary',
                        'submitForm': True,
                        'label': 'Create field'
                    }
                ]
            }
        ]

    methods = {
        'onSubmitForm':
            """(app, params) => {
                
            }"""
    }
