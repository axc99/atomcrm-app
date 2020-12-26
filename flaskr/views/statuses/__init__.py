from flask_babel import _

from flaskr.views.view import View, compile_js
from flaskr.models.status import get_status_colors

script = compile_js('script')


# Page: Statuses
class Statuses(View):
    def __init__(self):
        self.script = script
        self.meta = {
            'name': _('v_statuses_meta_name')
        }
        self.statuses = []
        self.data = {
            'statusColors': get_status_colors(),
            'strs': {
                'name': _('v_statuses_meta_name'),
                'header_createStatus': _('v_statuses_header_createStatus'),
                'schema_editStatus': _('v_statuses_schema_editStatus'),
                'schema_count_lead': _('v_statuses_schema_count_lead'),
                'schema_count_leads': _('v_statuses_schema_count_leads'),
                'schema_count_noLeads': _('v_statuses_schema_count_noLeads'),
                'schema_noStatuses': _('v_statuses_schema_noStatuses'),
                'schema_statusModal_createTitle': _('v_createStatus_meta_name'),
                'schema_statusModal_updateTitle': _('v_updateStatus_meta_name'),
                'schema_statusModal_form_name': _('v_createStatus_form_name'),
                'schema_statusModal_form_name_placeholder': _('v_createStatus_form_name_placeholder'),
                'schema_statusModal_form_name_length': _('v_createStatus_name_length'),
                'schema_statusModal_form_name_required': _('v_createStatus_name_required'),\
                'schema_statusModal_form_color': _('v_createStatus_form_color'),
                'schema_statusModal_form_color_required': _('v_createStatus_form_color_required'),
                'schema_statusModal_form_createBtn': _('v_createStatus_btn'),
                'schema_statusModal_form_saveBtn': _('v_updateStatus_btn'),
                'schema_deleteStatusModal_title': _('v_deleteStatus_header_title'),
                'schema_deleteStatusModal_subtitle': _('v_deleteStatus_header_subtitle'),
                'schema_deleteStatusModal_form_moveLeads': 'Move to {}',
                'schema_deleteStatusModal_form_deleteLeads': 'Delete leads',
                'schema_deleteStatusModal_form_btn': _('v_deleteStatus_schema_form_btn')
            }
        }
