import os
from datetime import timedelta
from flask_babel import _
import json

from flaskr import db
from flaskr.models.installation_extension_settings import InstallationExtensionSettings
from flaskr.views.view import View, get_method, method_with_vars, compile_js
from flaskr.models.lead import Lead
from flaskr.models.status import Status, get_hex_by_color, get_status_colors
from flaskr.models.installation_settings import InstallationSettings

script = compile_js('script')


# Page: Pipeline
class Pipeline(View):
    def __init__(self):
        View.__init__(self)
        self.meta = {
            'name': _('meta_name')
        }
        self.script = script
        self.data = {}

    def before(self, params, request_data):
        installation_settings = InstallationSettings.query \
            .filter_by(nepkit_installation_id=request_data['installation_id']) \
            .first()

        search = params.get('search', '').strip()

        filter_params = {
            'periodFrom': params['periodFrom'].replace('.', '-') if params.get('periodFrom') else None,
            'periodTo': params['periodTo'].replace('.', '-') if params.get('periodTo') else None,
            'archived': True if params.get('archived') == 'true' else False,
            'utmSource': params['utmSource'] if params.get('utmSource') else None,
            'utmMedium': params['utmMedium'] if params.get('utmMedium') else None,
            'utmCampaign': params['utmCampaign'] if params.get('utmCampaign') else None,
            'utmTerm': params['utmTerm'] if params.get('utmTerm') else None,
            'utmContent': params['utmContent'] if params.get('utmContent') else None,
        }
        filter_used = any(filter_params.values())

        has_any_integration = InstallationExtensionSettings.query \
            .filter_by(nepkit_installation_id=request_data['installation_id']) \
            .count() > 0

        statuses_q = db.session.execute("""  
            SELECT 
                s.*,
                (SELECT COUNT(*) FROM public.lead AS l WHERE l.status_id = s.id AND l.archived = false) AS lead_count,
                0 AS lead_amount_sum
            FROM 
                public.status AS s
            WHERE
                s.nepkit_installation_id = :installation_id
            ORDER BY 
                s.index""", {
            'installation_id': request_data['installation_id'],
            'amount_enabled': installation_settings.amount_enabled
        })

        statuses = []
        status_colors = get_status_colors()
        for status in statuses_q:
            status_lead_total = 0
            status_lead_amount_sum = 0

            status_color_hex = [c['hex'] for c in status_colors if c['key'] == status['color']]

            statuses.append({
                'id': status['id'],
                'name': status['name'],
                'lead_count': status_lead_total,
                'lead_amount_sum': status_lead_amount_sum,
                'color': status['color'],
                'colorHex': status_color_hex,
                'leads': []
            })

        currency = installation_settings.getCurrency()

        self.data = {
            'strs': {
                'header_title': _('v_pipeline_header_title'),
                'header_filter': _('v_pipeline_header_filter'),
                'header_autoCreate': _('v_pipeline_header_autoCreate'),
                'header_notifications': _('v_pipeline_header_notifications'),
                'header_search': _('v_pipeline_header_search'),
                'filterModal_title': _('v_pipeline_filterModal_title'),
                'filterModal_form_period': _('v_pipeline_filterModal_form_period'),
                'filterModal_form_archivedLeads': _('v_pipeline_filterModal_form_archivedLeads'),
                'filterModal_form_apply': _('v_pipeline_filterModal_form_apply'),
                'filterModal_form_clear': _('v_pipeline_filterModal_form_clear'),
                'notificationsSettingsModal_title': _('v_pipeline_notificationsSettingsModal_title'),
                'notificationsSettingsModal_changesSaved': _('v_pipeline_notificationsSettingsModal_changesSaved'),
                'notificationsSettingsModal_form_save': _('v_pipeline_notificationsSettingsModal_form_save'),
                'notificationsSettingsModal_form_notifications': _('v_pipeline_notificationsSettingsModal_form_notifications'),
                'notificationsSettingsModal_form_notifications_user': _('v_pipeline_notificationsSettingsModal_form_notifications_user'),
                'notificationsSettingsModal_form_notifications_extension': _('v_pipeline_notificationsSettingsModal_form_notifications_extension'),
                'notificationsSettingsModal_form_notifications_api': _('v_pipeline_notificationsSettingsModal_form_notifications_api'),
                'leadModal_title': _('v_pipeline_leadModal_title'),
                'leadModal_notification_changesSaved': _('v_pipeline_leadModal_notification_changesSaved'),
                'leadModal_save': _('v_pipeline_leadModal_save'),
                'leadModal_tags': _('v_pipeline_leadModal_tags'),
                'leadModal_comment': _('v_pipeline_leadModal_comment'),
                'leadModal_addDate': _('v_pipeline_leadModal_addDate'),
                'leadModal_updateDate': _('v_pipeline_leadModal_updateDate'),
                'leadModal_creator': _('v_pipeline_leadModal_creator'),
                "leadModal_utmMarks": _('v_pipeline_leadModal_utmMarks'),
                'leadModal_form_phone_rule': _('v_pipeline_leadModal_form_phone_rule'),
                'leadModal_form_email_rule': _('v_pipeline_leadModal_form_email_rule'),
                'leadModal_form_save': _('v_pipeline_leadModal_form_save'),
                'leadModal_form_restoreLead': _('v_pipeline_leadModal_form_restoreLead'),
                'leadModal_tabs_information': _('v_pipeline_leadModal_tabs_information'),
                'leadModal_tabs_tasks': _('v_pipeline_leadModal_tabs_tasks'),
                'leadModal_tabs_activity': _('v_pipeline_leadModal_tabs_activity'),
                "leadModal_select_selectOption": _('v_pipeline_leadModal_select_selectOption'),
                'getRegularDate_today': _('v_pipeline_getRegularDate_today'),
                'getRegularDate_yesterday': _('v_pipeline_getRegularDate_yesterday'),
                'getRegularDate_jan': _('v_pipeline_getRegularDate_jan'),
                'getRegularDate_feb': _('v_pipeline_getRegularDate_feb'),
                'getRegularDate_mar': _('v_pipeline_getRegularDate_mar'),
                'getRegularDate_apr': _('v_pipeline_getRegularDate_apr'),
                'getRegularDate_may': _('v_pipeline_getRegularDate_may'),
                'getRegularDate_jun': _('v_pipeline_getRegularDate_jun'),
                'getRegularDate_jul': _('v_pipeline_getRegularDate_jul'),
                'getRegularDate_aug': _('v_pipeline_getRegularDate_aug'),
                'getRegularDate_sep': _('v_pipeline_getRegularDate_sep'),
                'getRegularDate_oct': _('v_pipeline_getRegularDate_oct'),
                'getRegularDate_nov': _('v_pipeline_getRegularDate_nov'),
                'getRegularDate_dec': _('v_pipeline_getRegularDate_dec'),
                'board_archived': _('v_pipeline_board_archived')
            },

            'installationSettings': {
                'amountEnabled': installation_settings.amount_enabled,
                'currency': {
                    'formatString': currency['format_string'],
                    'rounding': currency['rounding'],
                    'decimalDigits': currency['decimal_digits']
                },
                'notificationsNewLeadUserEnabled': installation_settings.notifications_new_lead_user_enabled,
                'notificationsNewLeadExtensionEnabled': installation_settings.notifications_new_lead_extension_enabled,
                'notificationsNewLeadApiEnabled': installation_settings.notifications_new_lead_api_enabled
            },
            'search': search,
            'filterParams': filter_params,
            'filterUsed': filter_used,

            'hasAnyIntegration': has_any_integration,
            'autocreateCategoryId': os.environ.get('AUTOCREATE_CATEGORY_ID'),

            'statuses': statuses
        }
