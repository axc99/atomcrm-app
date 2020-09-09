from flaskr.views.view import View
from flaskr.models.status import Status, get_hex_by_color


# Window: Delete status
# If leads with deleted status exist
class DeleteStatus(View):
    meta = {
        'name': 'Delete status'
    }

    deleted_status = None
    other_statuses = []

    def before(self, params, request_data):
        id = params.get('id')

        if not id:
            raise Exception()

        self.deleted_status = Status.query \
            .filter_by(id=id,
                       veokit_installation_id=1) \
            .first()
        if not self.deleted_status:
            raise Exception()

        self.other_statuses = Status.query \
            .filter(Status.veokit_installation_id==1,
                    Status.id != id) \
            .order_by(Status.id.asc()) \
            .all()

    def get_header(self, params, request_data):
        return {
            'title': self.meta.get('name'),
            'subtitle': 'Leads with a deleted status exist. What to do with leads with the status «{}»?'.format(self.deleted_status.name)
        }

    def get_schema(self, params, request_data):
        select_options = [
            {
                'key': 'deleteLeads',
                'label': 'Delete leads'
            }
        ]

        for status in self.other_statuses:
            select_options.append({
                'key': status.id,
                'color': get_hex_by_color(status.color.name),
                'label': "Move leads to «{}»".format(status.name)
            })

        return [
            {
                '_com': 'Form',
                '_id': 'deleteStatusForm',
                'onFinish': 'onFinish',
                'fields': [
                    {
                        '_com': 'Field.Select',
                        'value': select_options[0]['key'] if len(select_options) > 0 else 'deleteLeads',
                        'options': select_options
                    }
                ],
                'buttons': [
                    {
                        '_com': 'Button',
                        'type': 'danger',
                        'submitForm': True,
                        'label': 'Delete status'
                    }
                ]
            }
        ]

    def get_methods(self, params, request_data):
        return {
            'onFinish':
                """(app, params, event) => {
                    const window = app.getView()
                    const form = window.getCom('deleteStatusForm')
                    const { values } = event
                    
                    let deleteLeads = false
                    let assignedStatusId = null
                    
                    if (values.action == 'deleteLeads') {
                        deleteLeads = True
                    } else {
                        assignedStatusId = values.action
                    }
                    
                    form.setAttr('loading', true)
                    
                    app
                        .sendReq('deleteStatus', {
                            statusId: """ + str(self.deleted_status.id) + """,
                            deleteLeads,
                            assignedStatusId
                        })
                        .then(result => {
                            form.setAttr('loading', false)
                            
                            if (result._res == 'ok') {
                                // Reload parent page
                                app.getPage().reload()
                            }
                        })
                }"""
        }
