from flaskr.views.pipeline import Pipeline
from flaskr.views.tasks import Tasks
from flaskr.views.statuses import Statuses
from flaskr.views.card import Card
from flaskr.views.api import Api
from flaskr.views.extensions.extension import Extension
from flaskr.views.analytics import Analytics

views_map = {
    # Pipeline
    'pipeline': Pipeline,

    # Statuses
    'statuses': Statuses,

    # Tasks
    'tasks': Tasks,

    # Card settings
    'card': Card,

    # Api
    'api': Api,

    # Extension
    'extension': Extension,

    # Analytics
    'analytics': Analytics
}
