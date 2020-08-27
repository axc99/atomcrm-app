from flaskr.views.view import View
from flaskr.models.status import Status


# Window: Update status
class UpdateStatus(View):
    status = None

    def before(self, params):
        id = params.get('id')

        if not id:
            raise Exception()

        self.status = Status.query\
                            .filter_by(id=id,
                                       veokit_system_id=1)\
                            .first()
        if not self.status:
            raise Exception()

    def get_header(self, params):
        return {
            'title': 'Edit status'
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
                        'value': self.status.name,
                        'maxLength': 20
                    }
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
                const { values } = params

                res = await app.sendReq('createStatus', { values })

                if (res.response) {
                    # Reload parent page with statuses
                    app.reloadPage()

                    # Close this modal
                    app.currentModal.close()
                }
            }"""
    }
