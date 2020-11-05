import enum
from flask_babel import _

from flaskr import db
from flaskr.views.view import View, get_method
from flaskr.models.task import Task, Task

compiled_methods = {
    'onDragTask': get_method('methods/onDragTask'),
    'deleteTask': get_method('methods/deleteTask')
}


# Page: Tasks
class Tasks(View):
    def __init__(self):
        self.meta = {
            'name': _('v_tasks_meta_name')
        }
        self.tasks = []

    def before(self, params, request_data):
        self.tasks = db.session.execute("""
            SELECT
                t.*,
                (SELECT COUNT(*) FROM public.task AS st WHERE st.parent_task_id = t.id) AS subtask_count
            FROM
                public.task AS t
            WHERE
                t.parent_task_id is null AND
                t.veokit_installation_id = :veokit_installation_id
            ORDER BY
                t.index""", {
            'veokit_installation_id': request_data['installation_id']
        })

    def get_header(self, params, request_data):
        return {
            'title': self.meta.get('name'),
            'actions': [
                {
                    '_com': 'Button',
                    'label': _('v_tasks_header_createTask'),
                    'type': 'primary',
                    'icon': 'plus',
                    'toWindow': 'createTask'
                }
            ]
        }

    def get_schema(self, params, request_data):
        list_items = []

        for task in self.tasks:
            list_items.append({
                'key': task.id,
                'title': task.name,
                'extra': "{} {}".format(task.subtask_count,
                                        _('v_tasksSets_schema_count_subtask') if task.subtask_count == 1 else _(
                                            'v_tasksSets_schema_count_subtasks')),
                'actions': [
                    {
                        '_com': 'Button',
                        'icon': 'edit',
                        'label': _('v_tasksSets_schema_edit'),
                        'toWindow': ['updateTask', {
                            'id': task.id
                        }]
                    },
                    {
                        '_com': 'Button',
                        'icon': 'delete',
                        'onClick': ['deleteTask', {
                            'id': task.id
                        }]
                    }
                ]
            })

        return [
            {
                '_com': 'List',
                '_id': 'tasksSetsList',
                'draggable': True,
                'emptyText': _('v_tasks_schema_noTasks'),
                'onDrag': 'onDragTask',
                'items': list_items
            }
        ]

    methods = compiled_methods
