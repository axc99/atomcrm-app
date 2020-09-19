from flaskr.views.view import View
from flaskr.models.status import Status, Status


# Window: Create status
class CreateStatus(View):
    meta = {
        'name': 'Create status'
    }

    def get_header(self, params, request_data):
        return {
            'title': self.meta.get('name')
        }

    def get_schema(self, params, request_data):
        color_options = [
            {'value': 'red', 'label': 'Red', 'color': '#E57373'},
            {'value': 'pink', 'label': 'Pink', 'color': '#F48FB1'},
            {'value': 'purple', 'label': 'Purple', 'color': '#9575CD'},
            {'value': 'blue', 'label': 'Blue', 'color': '#64B5F6'},
            {'value': 'green', 'label': 'Green', 'color': '#81C784'},
            {'value': 'orange', 'label': 'Orange', 'color': '#FFA726'}
        ]

        return [
            {
                '_com': 'Form',
                '_id': 'createStatusForm',
                'onFinish': 'onFinish',
                'fields': [
                    {
                        '_com': 'Field.Input',
                        'type': 'text',
                        'key': 'name',
                        'label': 'Status name',
                        'placeholder': 'Ex: In Progress',
                        'maxLength': 20,
                        'rules': [
                            { 'min': 2, 'max': 20, 'message': 'Must contain 2 - 20 chars' },
                            { 'required': True, 'message': 'Name is required' }
                        ]
                    },
                    {
                        '_com': 'Field.Select',
                        'value': 'red',
                        'key': 'color',
                        'label': 'Color',
                        'options': color_options,
                        'rules': [
                            {'required': True, 'message': 'Color is required'}
                        ]
                    }
                ],
                'buttons': [
                    {
                        '_com': 'Button',
                        'type': 'primary',
                        'submitForm': True,
                        'icon': 'plus',
                        'label': 'Create'
                    }
                ]
            }
        ]

    methods = {
        'onFinish':
            """(app, params, event) => {
                const window = app.getView()
                const form = window.getCom('createStatusForm')
                const { values } = event
                
                form.setAttr('loading', true)
                
                app
                    .sendReq('createStatus', {
                        name: values.name,
                        color: values.color
                    })
                    .then(result => {
                        form.setAttr('loading', false)
                        
                        if (result.res == 'ok') {
                            // Reload parent page
                            app.getPage().reload()
                        }
                    })
            }"""
    }
