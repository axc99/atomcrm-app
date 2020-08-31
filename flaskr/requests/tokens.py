from flaskr.secure import get_api_token


def get_token(data):
    token = get_api_token(1)

    return {
        'token': token
    }