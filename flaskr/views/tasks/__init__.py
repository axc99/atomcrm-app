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
                'schema_editTask': _('v_tasks_schema_editTask'),
                'schema_count_subtask': _('v_tasks_schema_count_subtask'),
                'schema_count_subtasks': _('v_tasks_schema_count_subtasks'),
                'schema_count_noTasks': _('v_tasks_schema_count_noTasks'),
                'schema_noTasks': _('v_tasks_schema_noTasks'),
                'schema_taskModal_createTitle': _('v_createTask_meta_name'),
                'schema_taskModal_updateTitle': _('v_updateTask_meta_name'),
                'schema_taskModal_form_name': _('v_createTask_form_name'),
                'schema_taskModal_form_name_placeholder': _('v_createTask_form_name_placeholder'),
                'schema_taskModal_form_name_length': _('v_createTask_name_length'),
                'schema_taskModal_form_name_required': _('v_createTask_name_required'),
                'schema_taskModal_form_color': _('v_createTask_form_color'),
                'schema_taskModal_form_color_required': _('v_createTask_form_color_required'),
                'schema_taskModal_form_createBtn': _('v_createTask_btn'),
                'schema_taskModal_form_saveBtn': _('v_updateTask_btn'),
                'schema_deleteTaskModal_title': _('v_deleteStatus_header_title'),
                'schema_deleteTaskModal_subtitle': _('v_deleteStatus_header_subtitle'),
                'schema_deleteTaskModal_delete': 'DElete'
            }
        }
    #
    # def before(self, params, request_data):
    #     self.tasks = db.session.execute("""
    #         SELECT
    #             t.*,
    #             (SELECT COUNT(*) FROM public.task AS st WHERE st.parent_task_id = t.id) AS subtask_count
    #         FROM
    #             public.task AS t
    #         WHERE
    #             t.parent_task_id is null AND
    #             t.nepkit_installation_id = :nepkit_installation_id
    #         ORDER BY
    #             t.index""", {
    #         'nepkit_installation_id': request_data['installation_id']
    #     })
    #
    # def get_header(self, params, request_data):
    #     return {
    #         'title': self.meta.get('name'),
    #         'actions': [
    #             {
    #                 '_com': 'Button',
    #                 'label': _('v_tasks_header_createTask'),
    #                 'type': 'primary',
    #                 'icon': 'plus',
    #                 'toWindow': 'createTask'
    #             }
    #         ]
    #     }
    #
    # def get_schema(self, params, request_data):
    #     list_items = []
    #
    #     for task in self.tasks:
    #         list_items.append({
    #             'key': task.id,
    #             'title': task.name,
    #             'extra': "{} {}".format(task.subtask_count,
    #                                     _('v_tasksSets_schema_count_subtask') if task.subtask_count == 1 else _(
    #                                         'v_tasksSets_schema_count_subtasks')),
    #             'actions': [
    #                 {
    #                     '_com': 'Button',
    #                     'icon': 'edit',
    #                     'label': _('v_tasksSets_schema_edit'),
    #                     'toWindow': ['updateTask', {
    #                         'id': task.id
    #                     }]
    #                 },
    #                 {
    #                     '_com': 'Button',
    #                     'icon': 'delete',
    #                     'onClick': ['deleteTask', {
    #                         'id': task.id
    #                     }]
    #                 }
    #             ]
    #         })
    #
    #     return [
    #         {
    #             '_com': 'List',
    #             '_id': 'tasksSetsList',
    #             'draggable': True,
    #             'emptyText': _('v_tasks_schema_noTasks'),
    #             'onDrag': 'onDragTask',
    #             'items': list_items
    #         }
    #     ]
    #
    # methods = compiled_methods
