from flask_babel import _

from flaskr.views.view import View, get_method, method_with_vars
from flaskr.models.task import Task

compiled_methods = {
    'onClickDeleteTask': get_method('methods/onClickDeleteTask'),
    'onDragTask': get_method('methods/onDragTask'),
    'onClickAddTask': get_method('methods/onClickAddTask'),
    'onFinishForm': get_method('methods/onFinishForm')
}


# Window: Update tasks set
class UpdateTask(View):
    def __init__(self):
        self.meta = {
            'name': _('v_updateTask_meta_name')
        }
        self.task = None
        self.tasks = []

    def before(self, params, request_data):
        self.task = Task.query \
            .filter_by(id=params['id'],
                       nepkit_installation_id=request_data['installation_id']) \
            .first()
        self.tasks = self.task.get_subtasks()

    def get_header(self, params, request_data):
        return {
            'title': self.meta.get('name')
        }

    def get_schema(self, params, request_data):
        table_rows = []
        task_index = 0
        for task in self.tasks:
            table_rows.append({
                'key': task['id'],
                'name': {
                    '_com': 'Field.Input',
                    'value': task['name']
                },
                'actions': [
                    {
                        '_com': 'Button',
                        'icon': 'delete',
                        'onClick': ['onClickDeleteTask', {
                            'index': task_index
                        }]
                    }
                ]
            })
            task_index += 1

        return [
            {
                '_com': 'Form',
                '_id': 'updateTaskForm',
                'onFinish': 'onFinishForm',
                'fields': [
                    {
                        '_com': 'Field.Input',
                        'type': 'text',
                        'key': 'name',
                        'label': _('v_updateTask_form_name'),
                        'value': self.task.name,
                        'placeholder': _('v_updateTask_form_name_placeholder'),
                        'maxLength': 50,
                        'rules': [
                            {'max': 50, 'message': _('v_updateTask_name_length')},
                            {'required': True, 'message': _('v_updateTask_name_required')}
                        ]
                    },
                    {
                        '_com': 'Field.Custom',
                        '_id': 'updateCardSettingsForm_tasks',
                        'label': _('v_updateTask_form_subtasks'),
                        'content': [
                            {
                                '_com': 'Table',
                                '_id': 'updateTaskForm_tasks_table',
                                'draggable': True,
                                'emptyText': _('v_updateTask_form_subtasks_table_noSubtasks'),
                                'onDrag': 'onDragTask',
                                'columns': [
                                    {
                                        'width': 35,
                                        'key': 'name'
                                    }
                                ],
                                'rows': table_rows
                            },
                            {
                                '_com': 'Button',
                                'label': _('v_updateTask_form_subtasks_addSubtask'),
                                'icon': 'plus',
                                'type': 'solid',
                                'onClick': 'onClickAddTask'
                            }
                        ]
                    }
                ],
                'buttons': [
                    {
                        '_com': 'Button',
                        'type': 'primary',
                        'submitForm': True,
                        'icon': 'save',
                        'label': _('v_updateTask_btn')
                    }
                ]
            }
        ]

    def get_methods(self, params, request_data):
        methods = compiled_methods.copy()

        methods['onFinishForm'] = method_with_vars(methods['onFinishForm'], {'TASK_ID': params['id']})

        return methods
