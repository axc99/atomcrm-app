from flaskr.views.view import View
from flaskr.models.field import Field, FieldType


# Window: Get token
class GetToken(View):
    meta = {
        'name': 'Get token'
    }

    def get_header(self, params):
        return {
            'title': self.meta.get('name')
        }

    def get_schema(self, params):
        return [
            'Your current token will be deactivated.',
            {
                '_id': 'getTokenBtn',
                '_com': 'Button',
                'label': 'Generate new token',
                'onClick': 'getToken'
            },
            {
                '_id': 'tokenInput',
                '_com': 'Field.Input',
                '_vis': False,
                'type': 'text',
                'readOnly': True
            }
        ]

    methods = {
        'getToken':
            """(app, params) => {
                const getTokenBtn = app.getById('getTokenBtn')
                const tokenInput = app.getById('tokenInput')
                
                tokenInput.setAttrs('loading', true)
                
                const res = await app.sendReq('getToken')
                tokenInput.setAttrs({
                    value: res.token,
                    _vis: true
                })
                
                tokenInput.setAttr('loading', false)
            }"""
    }
