from flask_babel import _
from flaskr.views.view import View
from flaskr.models.field import Field, FieldType


# Window: Get token
class GetToken(View):
    def __init__(self):
        self.meta = {
            'name': _('v_getToken_meta_name')
        }

    def get_header(self, params, request_data):
        return {
            'title': self.meta.get('name'),
            'subtitle': _('v_getToken_meta_header_subtitle')
        }

    def get_schema(self, params, request_data):
        return [
            {
                '_id': 'getTokenBtn',
                '_com': 'Button',
                'type': 'primary',
                'label': _('v_getToken_schema_btn'),
                'onClick': 'getToken'
            },
            {
                '_id': 'tokenInput',
                '_com': 'Field.Input',
                '_vis': False,
                'label': _('v_getToken_schema_token'),
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
                        if (result.res == 'ok') {
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
    }
