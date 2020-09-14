from flaskr.requests.leads import get_lead_components, create_lead, update_lead, update_lead_status, archive_lead, restore_lead
from flaskr.requests.statuses import create_status, update_status, update_status_index, delete_status
from flaskr.requests.fields import create_field, update_field, update_field_index, delete_field
from flaskr.requests.tokens import get_token


requests_map = {
    # Pipeline
    'getLeadComponents': get_lead_components,
    'createLead': create_lead,
    'updateLead': update_lead,
    'updateLeadStatus': update_lead_status,
    'archiveLead': archive_lead,
    'restoreLead': restore_lead,

    # Statuses
    'createStatus': create_status,
    'updateStatus': update_status,
    'updateStatusIndex': update_status_index,
    'deleteStatus': delete_status,

    # Fields
    'createField': create_field,
    'updateField': update_field,
    'updateFieldIndex': update_field_index,
    'deleteField': delete_field,

    # API
    'getToken': get_token
}
