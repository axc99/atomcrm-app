from flaskr.requests.leads import get_lead_components, create_lead, update_lead, update_lead_status, archive_lead, restore_lead, complete_lead_tasks
from flaskr.requests.statuses import create_status, update_status, update_status_index, delete_status
from flaskr.requests.tasks import create_task, update_task_index, update_task, delete_task
from flaskr.requests.tokens import get_token
from flaskr.requests.card_settings import update_card_settings
from flaskr.requests.extensions import update_extension_settings


requests_map = {
    # Pipeline
    'getLeadComponents': get_lead_components,
    'createLead': create_lead,
    'updateLead': update_lead,
    'updateLeadStatus': update_lead_status,
    'archiveLead': archive_lead,
    'restoreLead': restore_lead,
    'completeLeadTasks': complete_lead_tasks,

    # Statuses
    'createStatus': create_status,
    'updateStatus': update_status,
    'updateStatusIndex': update_status_index,
    'deleteStatus': delete_status,

    # Tasks
    'createTask': create_task,
    'updateTaskIndex': update_task_index,
    'updateTask': update_task,
    'deleteTask': delete_task,

    # Card settings
    'updateCardSettings': update_card_settings,

    # API
    'getToken': get_token,

    # Extensions
    'updateExtensionSettings': update_extension_settings
}
