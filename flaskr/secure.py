from secrets import choice
import string
from flaskr.models.token import Token


# Validate api token
def validate_api_token(token):
    is_token_valid = True

    veokit_system_id, token = token.split('_')

    if veokit_system_id and token:
        is_token_valid = Token.query \
            .filter_by(veokit_system_id=veokit_system_id,
                       token=token,
                       active=True) \
            .count() > 0

    # Return validation result and veokit_system_id
    return is_token_valid, veokit_system_id


# Get api token
def get_api_token(veokit_system_id):
    # Delete all tokens for this system
    Token.query\
        .filter_by(veokit_system_id=veokit_system_id)\
        .delete()

    # Create new token for this system
    token = Token()
    token.active = True
    token.token = ''.join([choice(string.ascii_uppercase + string.ascii_letters + string.digits) for _ in range(300)])
    token.veokit_system_id = veokit_system_id

    db.session.add(token)
    db.session.commit()

    return '{}_{}'.format(veokit_system_id, token.token)
