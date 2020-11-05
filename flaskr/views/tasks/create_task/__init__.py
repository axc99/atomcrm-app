from flask_babel import _

from flaskr.views.view import View, get_method
from flaskr.models.status import Status, get_status_colors

compiled_methods = {
    'onClickDeleteTask': get_method('methods/onClickDeleteTask'),
    'onDragTask': get_method('methods/onDragTask'),
    'onClickAddTask': get_method('methods/onClickAddTask'),
    'onFinishForm': get_method('methods/onFinishForm')
}


# Window: Create tasks set
class CreateTask(View):
    def __init__(self):
        self.meta = {
            'name': _('v_createTask_meta_name')
        }

    def get_header(self, params, request_data):
        return {
            'title': self.meta.get('name')
        }

    def get_schema(self, params, request_data):
        return [
            {
                '_com': 'Form',
                '_id': 'createTaskForm',
                'onFinish': 'onFinishForm',
                'fields': [
                    {
                        '_com': 'Field.Input',
                        'type': 'text',
                        'key': 'name',
                        'label': _('v_createTask_form_name'),
                        'placeholder': _('v_createTask_form_name_placeholder'),
                        'maxLength': 50,
                        'rules': [
                            {'max': 50, 'message': _('v_createTask_name_length')},
                            {'required': True, 'message': _('v_createTask_name_required')}
                        ]
                    },
                    {
                        '_com': 'Field.Custom',
                        '_id': 'updateCardSettingsForm_tasks',
                        'label': _('v_createTask_form_subtasks'),
                        'content': [
                            {
                                '_com': 'Table',
                                '_id': 'createTaskForm_tasks_table',
                                'draggable': True,
                                'emptyText': _('v_updateTask_form_subtasks_table_noSubtasks'),
                                'onDrag': 'onDragTask',
                                'columns': [
                                    {
                                        'width': 35,
                                        'key': 'name'
                                    }
                                ],
                                'rows': []
                            },
                            {
                                '_com': 'Button',
                                'label': _('v_createTask_form_subtasks_addSubtask'),
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
                        'icon': 'plus',
                        'label': _('v_createTask_btn')
                    }
                ]
            }
        ]

    methods = compiled_methods
