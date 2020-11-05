from flaskr.views.leads.pipeline import Pipeline
from flaskr.views.leads.update_lead import UpdateLead
from flaskr.views.leads.filter import Filter
from flaskr.views.tasks.tasks import Tasks
from flaskr.views.tasks.create_task import CreateTask
from flaskr.views.tasks.update_task import UpdateTask
from flaskr.views.statuses.statuses import Statuses
from flaskr.views.statuses.create_status import CreateStatus
from flaskr.views.statuses.update_status import UpdateStatus
from flaskr.views.statuses.delete_status import DeleteStatus
from flaskr.views.card.card import Card
from flaskr.views.api.api import Api
from flaskr.views.api.get_token import GetToken
from flaskr.views.extensions.extension import Extension

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

    # Tasks
    'tasks': Tasks,
    'createTask': CreateTask,
    'updateTask': UpdateTask,

    # Card settings
    'card': Card,

    # Api
    'api': Api,
    'getToken': GetToken,

    # Extension
    'extension': Extension
}
