from flaskr.views.view import View
from flaskr.models.status import Status


# Window: Delete status
# If leads with deleted status exist
class DeleteStatus(View):
    meta = {
        'name': 'Delete status'
    }

    deleted_status = None
    other_statuses = []

    def before(self, params):
        id = params.get('id')

        if not id:
            raise Exception()

        self.deleted_status = Status.query \
            .filter_by(id=id,
                       veokit_system_id=1) \
            .first()
        if not self.deleted_status:
            raise Exception()

        self.other_statuses = Status.query \
            .filter(Status.veokit_system_id==1,
                    Status.id != id) \
            .order_by(Status.id.asc()) \
            .all()

    def get_header(self, params):
        return {
            'title': self.meta.get('name'),
            'subtitle': 'Leads with a deleted status exist. What to do with leads with the status «{}»?'.format(self.deleted_status.name)
        }

    def get_schema(self, params):
        select_options = [
            {
                'key': 'deleteLeads',
                'label': 'Delete leads'
            }
        ]

        for status in self.other_statuses:
            select_options.append({
                'key': status.id,
                'label': "Move leads to «{}»".format(status.name)
            })

        return [
            {
                '_com': 'Form',
                'onSubmit': 'onSubmitForm',
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

    def get_methods(self, params):
        return {
            'onSubmitForm':
                """(app, params) => {
                    const { values } = params
                    
                    let deleteLeads = false
                    let assignStatusId = null
                    
                    if (values.action == 'deleteLeads') {
                        deleteLeads = True
                    } else {
                        assignStatusId = values.action
                    }
    
                    res = await app.sendReq('deleteStatus', { 
                        id: """ + str(self.deleted_status.id) + """,
                        deleteLeads,
                        assignedStatusId
                    })
    
                    if (res.response) {
                        # Reload parent page with statuses
                        app.reloadPage()
                    }
                }"""
        }
