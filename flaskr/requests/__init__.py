from flaskr.requests.leads import get_leads, get_lead, create_lead, update_lead, update_lead_status, archive_lead, restore_lead, complete_lead_tasks, get_lead_actions
from flaskr.requests.statuses import get_statuses, create_status, update_status, update_status_index, delete_status
from flaskr.requests.tasks import get_tasks, create_task, update_task_index, update_task, delete_task
from flaskr.requests.tokens import get_token
from flaskr.requests.card_settings import update_card_settings, get_fields
from flaskr.requests.extensions import update_extension_settings
from flaskr.requests.handlers import handle_install_app, handle_uninstall_app, handle_enable_extension, handle_disable_extension


requests_map = {
    # Handle events
    'handleInstallApp': handle_install_app,
    'handleUninstallApp': handle_uninstall_app,
    'handleEnableExtension': handle_enable_extension,
    'handleDisableExtension': handle_disable_extension,

    # Pipeline
    'getLeads': get_leads,
    'getLead': get_lead,
    'getLeadActions': get_lead_actions,
    'createLead': create_lead,
    'updateLead': update_lead,
    'updateLeadStatus': update_lead_status,
    'archiveLead': archive_lead,
    'restoreLead': restore_lead,
    'completeLeadTasks': complete_lead_tasks,

    # Statuses
    'getStatuses': get_statuses,
    'createStatus': create_status,
    'updateStatus': update_status,
    'updateStatusIndex': update_status_index,
    'deleteStatus': delete_status,

    # Tasks
    'getTasks': get_tasks,
    'createTask': create_task,
    'updateTaskIndex': update_task_index,
    'updateTask': update_task,
    'deleteTask': delete_task,

    # Card settings
    'updateSettings': update_card_settings,
    'getFields': get_fields,

    # API
    'getToken': get_token,

    # Extensions
    'updateExtensionSettings': update_extension_settings
}
