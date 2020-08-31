from flaskr.requests.statuses import create_status, update_status, update_statuses, delete_status
from flaskr.requests.tokens import get_token

requests_map = {
    # Statuses
    'createStatus': create_status,
    'updateStatus': update_status,
    'updateStatuses': update_statuses,
    'deleteStatus': delete_status,

    # Tokens
    'getToken': get_token
}
