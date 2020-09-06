from flaskr.views.view import View
from flaskr.models.field import Field, FieldType


# Window: Get token
class GetToken(View):
    meta = {
        'name': 'Get token'
    }

    def get_header(self, params, request_data):
        return {
            'title': self.meta.get('name'),
            'subtitle': 'Your current token will be deactivated.'
        }

    def get_schema(self, params, request_data):
        return [
            {
                '_id': 'getTokenBtn',
                '_com': 'Button',
                'type': 'primary',
                'label': 'Generate new token',
                'onClick': 'getToken'
            },
            {
                '_id': 'tokenInput',
                '_com': 'Field.Input',
                '_vis': False,
                'label': 'New token',
                'multiline': True,
                'type': 'text',
                'readOnly': True
            }
        ]

    methods = {
        'getToken':
            """(app, params, e) => {
                const view = app.getView()
                const getTokenBtn = view.getCom('getTokenBtn')
                const tokenInput = view.getCom('tokenInput')
                
                getTokenBtn.setAttr('loading', true)
                
                // Get new token
                app
                    .sendReq('getToken', {})
                    .then(result => {
                        if (result._res == 'ok') {
                            tokenInput.setAttrs({
                                _vis: true,
                                value: result.token
                            })
                        
                            getTokenBtn.setAttrs({
                                _vis: false,
                                loading: false
                            })
                        }
                    })
            }"""

        # const getTokenBtn = app.getById('getTokenBtn')
        # const tokenInput = app.getById('tokenInput')
        #
        # tokenInput.setAttrs('loading', true)
        #
        # const res = await app.sendReq('getToken')
        # tokenInput.setAttrs({
        #     value: res.token,
        #     _vis: true
        # })
        #
        # tokenInput.setAttr('loading', false)
    }
