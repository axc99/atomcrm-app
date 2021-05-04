import base64
import os
from secrets import choice
import string
from flaskr.models.token import Token
from flaskr import db


# Validate secret key
def validate_secret_key(secret_key):
    return secret_key == os.environ.get('APP_SECRET_KEY')


# Validate api token
def validate_api_token(token):
    if not token:
        return False, None

    is_token_valid = True

    try:
        token = base64.b64decode(token.encode()).decode()
    except Exception as e:
        print(e)
        return False, None
    nepkit_installation_id, token = token.split(':')

    if nepkit_installation_id and token:
        is_token_valid = Token.query \
            .filter_by(nepkit_installation_id=nepkit_installation_id,
                       token=token,
                       active=True) \
            .count() > 0

    # Return validation result and nepkit_installation_id
    return is_token_valid, nepkit_installation_id


# Get api token
def get_api_token(nepkit_installation_id):
    # Delete all tokens for this installation
    Token.query\
        .filter_by(nepkit_installation_id=nepkit_installation_id)\
        .delete()

    # Create new token for this installation
    token = Token()
    token.active = True
    token.token = ''.join([choice(string.ascii_uppercase + string.ascii_letters + string.digits) for _ in range(300)])
    token.nepkit_installation_id = nepkit_installation_id

    db.session.add(token)
    db.session.commit()

    return base64.b64encode('{}:{}'.format(nepkit_installation_id, token.token).encode()).decode()
