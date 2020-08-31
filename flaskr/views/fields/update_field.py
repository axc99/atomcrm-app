from flaskr.views.view import View
from flaskr.models.field import Field


# Window: Update field
class UpdateField(View):
    field = None

    def before(self, params):
        id = params.get('id')

        if not id:
            raise Exception()

        self.field = Field.query \
            .filter_by(id=id,
                       veokit_system_id=1) \
            .first()
        if not self.field:
            raise Exception()

    def get_header(self, params):
        return {
            'title': 'Edit field'
        }

    def get_schema(self, params):
        return [
            {
                '_com': 'Form',
                'onSubmit': 'onSubmitForm',
                'fields': [

                ],
                'buttons': [
                    {
                        '_com': 'Button',
                        'type': 'primary',
                        'submitForm': True,
                        'label': 'Save changes'
                    }
                ]
            }
        ]

    methods = {
        'onSubmitForm':
            """(app, params) => {
                
            }"""
    }
