from flaskr.requests.statuses import create_status, update_status, update_statuses, delete_status

requests_map = {
    # Statuses
    'createStatus': create_status,
    'updateStatus': update_status,
    'updateStatuses': update_statuses,
    'deleteStatus': delete_status
}
