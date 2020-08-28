from flaskr.views.pipeline.pipeline import Pipeline
from flaskr.views.statuses.statuses import Statuses
from flaskr.views.statuses.create_status import CreateStatus
from flaskr.views.statuses.update_status import UpdateStatus
from flaskr.views.statuses.delete_status import DeleteStatus
from flaskr.views.fields.fields import Fields
from flaskr.views.api.api import Api

views_map = {
    # Pipeline
    'pipeline': Pipeline,

    # Statuses
    'statuses': Statuses,
    'createStatus': CreateStatus,
    'updateStatus': UpdateStatus,
    'deleteStatus': DeleteStatus,

    # Fields
    'fields': Fields,

    # Api
    'api': Api
}
