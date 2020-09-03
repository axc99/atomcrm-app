from flaskr.views.view import View
from flaskr.models.status import Status


# Page: Statuses
class Statuses(View):
    meta = {
        'name': 'Statuses'
    }

    statuses = []

    def before(self, params):
        self.statuses = Status.query \
            .filter_by(veokit_system_id=1) \
            .order_by(Status.index.asc()) \
            .all()

    def get_header(self, params):
        return {
            'title': self.meta.get('name'),
            'actions': [
                {
                    '_com': 'Button',
                    'label': 'Create status',
                    'type': 'primary',
                    'icon': 'plus',
                    'toWindow': 'createStatus'
                }
            ]
        }

    def get_schema(self, params):
        list_items = []

        for status in self.statuses:
            deleteButton = {
                '_com': 'Button',
                'icon': 'delete'
            }

            # If leads with deleted status exist
            if True:
                deleteButton['toWindow'] = ['deleteStatus', {
                    'id': status.id
                }]
            else:
                deleteButton['openModal'] = {
                    'title': 'Delete status',
                    'description': 'Are you sure you want to delete this status?',
                    'okText': 'Delete',
                    'onOk': ['deleteStatus', {
                        'id': status.id
                    }]
                }

            list_items.append({
                'key': status.id,
                'title': status.name,
                'actions': [
                    {
                        '_com': 'Button',
                        'icon': 'edit',
                        'label': 'Edit status',
                        'toWindow': ['updateStatus', {
                            'id': status.id
                        }]
                    },
                    deleteButton
                ]
            })

        return [
            {
                '_com': 'List',
                'sortable': True,
                'onSort': 'onSortStatuses',
                'items': list_items
            }
        ]

    methods = {
        # 'onSortStatuses':
        #     """(app, params) => {
        #         const statuses = []
        #
        #         params.items.map((item, itemIndex) => {
        #             statuses.push({
        #                 id: item.key,
        #                 values: {
        #                     index: itemIndex
        #                 }
        #             })
        #         })
        #
        #         res = await app.sendReq('updateStatuses', {
        #             statuses
        #         })
        #     }""",
        # 'deleteStatus':
        #     """(app, params) => {
        #         const { id, assignedStatusId } = params
        #
        #         app.modal.setAttr('okLoading', true)
        #
        #         res = await app.sendReq('deleteStatus', {
        #             statusId: id,
        #             assignedStatusId
        #         })
        #
        #         app.modal.setAttr('okLoading', false)
        #
        #         # Reload parent page with statuses
        #         app.reloadPage()
        #     }"""
    }
