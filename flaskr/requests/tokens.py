from flaskr.secure import get_api_token


def get_token(params, request_data):
    token = get_api_token(request_data['installation_id'])

    return {
        'res': 'ok',
        'token': token
    }