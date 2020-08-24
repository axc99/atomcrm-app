 from flaskr.views.view import View

 class Statuses(View):
    meta = {
        'name': 'Statuses'
    }

    method_map = {
        'onSortStatuses': 'statuses/onSortStatuses.js'
    }

    def get_header(self):
        return None

    def get_schema(self):
        return None
