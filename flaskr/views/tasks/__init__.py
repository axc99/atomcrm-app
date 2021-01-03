import enum
from flask_babel import _

from flaskr import db
from flaskr.views.view import View, compile_js

script = compile_js('script')


# Page: Tasks
class Tasks(View):
    def __init__(self):
        self.script = script
        self.meta = {
            'name': _('v_tasks_meta_name')
        }
        self.tasks = []
        self.data = {
            'strs': {
                'name': _('v_tasks_meta_name'),
                'header_createTask': _('v_tasks_header_createTask'),
                'table_editTask': _('v_tasks_table_editTask'),
                'table_count_subtask': _('v_tasks_table_count_subtask'),
                'table_count_subtasks': _('v_tasks_table_count_subtasks'),
                'table_count_noTasks': _('v_tasks_table_count_noTasks'),
                'table_noTasks': _('v_tasks_table_noTasks'),
                'taskModal_createTitle': _('v_tasks_taskModal_createTitle'),
                'taskModal_updateTitle': _('v_tasks_taskModal_updateTitle'),
                'taskModal_form_name': _('v_tasks_taskModal_form_name'),
                'taskModal_form_name_placeholder': _('v_tasks_taskModal_form_name_placeholder'),
                'taskModal_form_name_length': _('v_tasks_taskModal_form_name_length'),
                'taskModal_form_name_required': _('v_tasks_taskModal_form_name_required'),
                'taskModal_form_subtasks': _('v_tasks_taskModal_form_subtasks'),
                'taskModal_form_subtasks_table_noSubtasks': _('v_tasks_taskModal_form_subtasks_table_noSubtasks'),
                'taskModal_form_subtasks_addSubtask': _('v_tasks_taskModal_form_subtasks_addSubtask'),
                'taskModal_form_create': _('v_tasks_taskModal_form_create'),
                'taskModal_form_save': _('v_tasks_taskModal_form_save'),
                'deleteTaskModal_title': _('v_tasks_deleteTaskModal_title'),
                'deleteTaskModal_subtitle': _('v_tasks_deleteTaskModal_subtitle'),
                'deleteTaskModal_delete': _('v_tasks_deleteTaskModal_delete')
            }
        }
