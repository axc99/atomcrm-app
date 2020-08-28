from flaskr.views.view import View
from flaskr.models.tag import Tag


# Page: Tags
class Tags(View):
    meta = {
        'name': 'Tags'
    }

    tags = []

    def before(self, params):
        self.tags = Tag.query \
            .filter_by(veokit_system_id=1) \
            .all()

    def get_header(self, params):
        return {
            'title': self.meta.get('name'),
            'actions': [
                {
                    '_com': 'Button',
                    'label': 'Add tag',
                    'type': 'primary',
                    'icon': 'plus',
                    'toWindow': 'createTag'
                }
            ]
        }

    def get_schema(self, params):
        list_items = []

        for tag in self.tags:
            list_items.append({
                'id': status.id,
                'title': status.name,
                'actions': [
                    {
                        '_com': 'Button',
                        'icon': 'edit',
                        'label': 'Edit',
                        'toWindow': ['status', {
                            'id': status.id
                        }]
                    },
                    {
                        '_com': 'Button',
                        'icon': 'delete',
                        'openModal': {
                            'title': 'Delete tag',
                            'description': '',
                            'okText': 'Are you sure you want to remove this tag?',
                            'onOk': ['deleteStatus', {
                                'id': status.id
                            }]
                        }
                    }
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
        'onSortStatuses':
            """(app, params) => {
                const statuses = []

                params.items.map((item, itemIndex) => {
                    statuses.push({
                        id: item.key,
                        values: {
                            index: itemIndex
                        }
                    })
                })

                res = await app.sendReq('updateStatuses', { 
                    statuses 
                })  
            }""",
        'deleteStatus':
            """(app, params) => {
                const { id, assignedStatusId } = params

                app.modal.setAttr('okLoading', true)

                res = await app.sendReq('deleteStatus', {
                    statusId: id,
                    assignedStatusId
                })

                app.modal.setAttr('okLoading', false)

                # Reload parent page with statuses
                app.reloadPage()
            }"""
    }
