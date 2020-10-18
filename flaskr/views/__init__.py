from flaskr.views.pipeline.pipeline import Pipeline
from flaskr.views.pipeline.update_lead import UpdateLead
from flaskr.views.pipeline.filter import Filter
from flaskr.views.statuses.statuses import Statuses
from flaskr.views.statuses.create_status import CreateStatus
from flaskr.views.statuses.update_status import UpdateStatus
from flaskr.views.statuses.delete_status import DeleteStatus
from flaskr.views.card.card import Card
from flaskr.views.api.api import Api
from flaskr.views.api.getToken import GetToken

views_map = {
    # Pipeline
    'pipeline': Pipeline,
    'updateLead': UpdateLead,
    'filter': Filter,

    # Statuses
    'statuses': Statuses,
    'createStatus': CreateStatus,
    'updateStatus': UpdateStatus,
    'deleteStatus': DeleteStatus,

    # Card settings
    'card': Card,

    # Api
    'api': Api,
    'getToken': GetToken
}
