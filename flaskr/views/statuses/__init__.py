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
                'list_editStatus': _('v_statuses_list_editStatus'),
                'list_count_lead': _('v_statuses_list_count_lead'),
                'list_count_leads': _('v_statuses_list_count_leads'),
                'list_count_noLeads': _('v_statuses_list_count_noLeads'),
                'list_noStatuses': _('v_statuses_list_noStatuses'),
                'statusModal_createTitle': _('v_statuses_statusModal_createTitle'),
                'statusModal_updateTitle': _('v_statuses_statusModal_updateTitle'),
                'statusModal_form_name': _('v_statuses_statusModal_form_name'),
                'statusModal_form_name_placeholder': _('v_statuses_statusModal_form_name_placeholder'),
                'statusModal_form_name_length': _('v_statuses_statusModal_form_name_length'),
                'statusModal_form_name_required': _('v_statuses_statusModal_form_name_required'),
                'statusModal_form_color': _('v_statuses_statusModal_form_color'),
                'statusModal_form_color_required': _('v_statuses_statusModal_form_color_required'),
                'statusModal_form_createBtn': _('v_statuses_statusModal_form_create'),
                'statusModal_form_saveBtn': _('v_statuses_statusModal_form_save'),
                'deleteStatusModal_title': _('v_statuses_deleteStatusModal_title'),
                'deleteStatusModal_subtitle': _('v_statuses_deleteStatusModal_subtitle'),
                'deleteStatusModal_form_moveLeads': _('v_statuses_deleteStatusModal_form_moveLeads'),
                'deleteStatusModal_form_deleteLeads': _('v_statuses_deleteStatusModal_form_deleteLeads'),
                'deleteStatusModal_form_delete': _('v_statuses_deleteStatusModal_form_delete')
            }
        }
