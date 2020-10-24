from cerberus import Validator

from flaskr import db
from flaskr.models.status import Status
from flaskr.models.installation_extension_settings import InstallationExtensionSettings


# Update extension
def update_extension_settings(params, request_data):
    vld = Validator({
        'extensionId': {'type': 'number', 'required': True},
        'data': {'type': 'dict', 'required': True}
    })
    is_valid = vld.validate(params)
    if not is_valid:
        return {'res': 'err', 'message': 'Invalid params', 'errors': vld.errors}

    integ_settings = InstallationExtensionSettings.query \
        .filter_by(id=params['extensionId']) \
        .first()
    integ_settings.data = params['data']
    db.session.commit()

    return {
        'res': 'ok'
    }
