from flaskr.views.statuses.statuses import Statuses
from flaskr.views.statuses.create_status import CreateStatus
from flaskr.views.statuses.update_status import UpdateStatus
from flaskr.views.statuses.delete_status import DeleteStatus

views_map = {
    # Statuses
    'statuses': Statuses,
    'createStatus': CreateStatus,
    'updateStatus': UpdateStatus,
    'deleteStatus': DeleteStatus
}
