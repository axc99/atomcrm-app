from flaskr.requests.statuses import create_status, update_status, update_status_index, delete_status
from flaskr.requests.fields import create_field, update_field, delete_field
from flaskr.requests.tokens import get_token
requests_map = {
    # Pipeline
    # ...

    # Statuses
    'createStatus': create_status,
    'updateStatus': update_status,
    'updateStatusIndex': update_status_index,
    'deleteStatus': delete_status,

    # Fields
    'createField': create_field,
    'updateField': update_field,
    'deleteField': delete_field,

    # API
    'getToken': get_token
}

