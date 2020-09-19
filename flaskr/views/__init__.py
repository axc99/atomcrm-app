from flaskr.views.pipeline.pipeline import Pipeline
from flaskr.views.pipeline.update_lead import UpdateLead
from flaskr.views.pipeline.search_info import SearchInfo
from flaskr.views.statuses.statuses import Statuses
from flaskr.views.statuses.create_status import CreateStatus
from flaskr.views.statuses.update_status import UpdateStatus
from flaskr.views.statuses.delete_status import DeleteStatus
from flaskr.views.fields.fields import Fields
from flaskr.views.fields.create_field import CreateField
from flaskr.views.fields.update_field import UpdateField
from flaskr.views.api.api import Api
from flaskr.views.api.getToken import GetToken

views_map = {
    # Pipeline
    'pipeline': Pipeline,
    'updateLead': UpdateLead,
    'searchInfo': SearchInfo,

    # Statuses
    'statuses': Statuses,
    'createStatus': CreateStatus,
    'updateStatus': UpdateStatus,
    'deleteStatus': DeleteStatus,

    # Fields
    'fields': Fields,
    'createField': CreateField,
    'updateField': UpdateField,

    # Api
    'api': Api,
    'getToken': GetToken
}
