from flaskr.views.view import View
from flaskr.models.status import Status


# Window: Create status
class CreateStatus(View):
    meta = {
        'name': 'Create status'
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
                'fields': [
                    {
                        '_com': 'Field.Input',
                        'type': 'text',
                        'key': 'name',
                        'label': 'Status label',
                        'placeholder': 'Ex: In progress',
                        'maxLength': 20
                    }
                ],
                'buttons': [
                    {
                        '_com': 'Button',
                        'type': 'primary',
                        'submitForm': True,
                        'label': 'Create status'
                    }
                ]
            }
        ]

    methods = {
        'onSubmitForm':
            """(app, values) => {
                console.log('values', values)
                
            }"""
    }

    # const { values } = params
    #
    # res = await app.sendReq('createStatus', { values })
    #
    # if (res.response) {
    #     # Reload parent page with statuses
    #     app.reloadPage()
    # }
