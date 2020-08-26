from flaskr.views.view import View
from flaskr.models.status import Status


class Statuses(View):
    meta = {
        'name': 'Statuses'
    }

    def get_header(self):
        return {
            'name': self.meta.get('name'),
            'actions': [
                {
                    '_com': 'Button',
                    'label': 'Create',
                    'toWindow': 'createStatus'
                }
            ]
        }

    def get_schema(self):
        list_items = []

        statuses = Status.query\
            .filter_by(veokit_system_id=1)\
            .all()

        for status in statuses:
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
                        'toWindow': ['deleteStatus', {
                            'id': status.id
                        }]
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
                const { key, newIndex, oldIndex } = params.movedItem

                res = await app.sendReq('updateStatus', {
                    key,
                    data: {
                        newIndex,
                        oldIndex
                    }
                })
            }"""
    }
