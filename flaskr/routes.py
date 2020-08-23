from flaskr import app
from flaskr.views import views_map


# Index page
@app.route('/')
def index():
    return 'Atom CRM <a href="https://veokit.com/store/1-veokit-team/1-atomcrm">VeoKit App</a>'

# Get view
# Request endpoint: /api
@app.route('/api', methods=['POST'])
def request():
    data = request.get_json()

    if data['_req'] == 'getView':
        view_key = data['key']
        view = views_map[view_key]

        view_meta = view.meta
        view_methods = view.methods
        view_header = view.get_header()
        view_schema = view.get_view()

        return {
            'meta': view_meta,
            'methods': view_methods,
            'header': view_header,
            'schema': view_schema
        }

    elif data._req == 'getViewUpdate':
        pass

    return {}


# Get view
# Request web hook: /webhook
@app.route('/api', methods=['POST'])
def webhook():
    data = request.get_json()

    return 'webhook'
