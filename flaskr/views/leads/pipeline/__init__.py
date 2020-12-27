import os
from datetime import timedelta
from flask_babel import _
import json

from flaskr import db
from flaskr.models.installation_extension_settings import InstallationExtensionSettings
from flaskr.views.view import View, get_method, method_with_vars, compile_js
from flaskr.models.lead import Lead
from flaskr.models.status import Status, get_hex_by_color, get_status_colors
from flaskr.models.installation_card_settings import InstallationCardSettings

script = compile_js('script')


# Page: Pipeline
class Pipeline(View):
    def __init__(self):
        self.script = script
        self.meta = {
            'name': _('v_pipeline_meta_name')
        }
        self.data = {
            'statuses': [],
            'strs': {
                'schema_header_title': 'PIPELINE'
            }
        }
        self.leads = []
        self.statuses = []
        self.installation_card_settings = None
        self.filter_used = False
        self.filter_params = {}
        self.has_any_integration = False

    def before(self, params, request_data):
        installation_card_settings = InstallationCardSettings.query \
            .filter_by(nepkit_installation_id=request_data['installation_id']) \
            .first()

        self.data['installationCardSettings'] = {
            'amountEnabled': installation_card_settings.amount_enabled,
            'currency': installation_card_settings.currency.name
        }
        self.data['search'] = params.get('search')
        self.data['filterParams'] = {
            'periodFrom': params['periodFrom'].replace('.', '-') if params.get('periodFrom') else None,
            'periodTo': params['periodTo'].replace('.', '-') if params.get('periodTo') else None,
            'archived': True if params.get('archived') == 'true' else False,
            'utmSource': params['utmSource'] if params.get('utmSource') else None,
            'utmMedium': params['utmMedium'] if params.get('utmMedium') else None,
            'utmCampaign': params['utmCampaign'] if params.get('utmCampaign') else None,
            'utmTerm': params['utmTerm'] if params.get('utmTerm') else None,
            'utmContent': params['utmContent'] if params.get('utmContent') else None,
        }
        self.data['filterUsed'] = any(self.data['filterParams'].values())

        statuses_q = db.session.execute("""  
            SELECT 
                s.*,
                (SELECT COUNT(*) FROM public.lead AS l WHERE l.status_id = s.id AND l.archived = false) AS lead_count,
                123456 AS lead_amount_sum
            FROM 
                public.status AS s
            WHERE
                s.nepkit_installation_id = :installation_id
            ORDER BY 
                s.index""", {
            'installation_id': request_data['installation_id'],
            'amount_enabled': installation_card_settings.amount_enabled
        })

        self.data['hasAnyIntegration'] = InstallationExtensionSettings.query \
            .filter_by(nepkit_installation_id=request_data['installation_id']) \
            .count() > 0
        self.data['autocreateCategoryId'] = os.environ.get('AUTOCREATE_CATEGORY_ID')


        self.data['statuses'] = []
        status_colors = get_status_colors()
        for status in statuses_q:
            # leads_q = Lead.get_with_filter(installation_id=request_data['installation_id'],
            #                                status_id=status['id'],
            #                                search=params.get('search'),
            #                                offset=0,
            #                                limit=10,
            #                                filter=self.filter_params)
            #
            # status_leads = []
            status_lead_total = 0
            status_lead_amount_sum = 0

            status_color_hex = [c['hex'] for c in status_colors if c['key'] == status['color']]
            #
            # for lead in leads_q:
            #     if status_lead_total == 0:
            #         status_lead_total = lead.total
            #     if status_lead_amount_sum == 0:
            #         status_lead_amount_sum = lead.amount_sum
            #
            #     status_leads.append({
            #         'id': lead.id,
            #         'uid': lead.uid,
            #         'status_id': lead.status_id,
            #         'amount': lead.amount,
            #         'archived': lead.archived,
            #         'add_date': (lead.add_date + timedelta(minutes=request_data['timezone_offset'])).strftime('%Y-%m-%d %H:%M:%S'),
            #         'fields': Lead.get_fields(lead.id),
            #         'tags': Lead.get_tags(lead.id)
            #     })

            self.data['statuses'].append({
                'id': status['id'],
                'name': status['name'],
                'lead_count': status_lead_total,
                'lead_amount_sum': status_lead_amount_sum,
                'color': status['color'],
                'colorHex': status_color_hex,
                'leads': []
            })

    def get_header(self, params, request_data):
        header = {
            'title': self.meta.get('name'),
            'actions': [
                {
                    '_com': 'Button',
                    'icon': 'filter',
                    'label': _('v_pipeline_header_filter'),   # 'Filter',
                    'toWindow': ['filter', {
                        'periodFrom': self.filter_params.get('period_from'),
                        'periodTo': self.filter_params.get('period_to'),
                        'archived': self.filter_params.get('archived'),
                        'utmSource': self.filter_params.get('utm_source'),
                        'utmMedium': self.filter_params.get('utm_medium'),
                        'utmCampaign': self.filter_params.get('utm_campaign'),
                        'utmTerm': self.filter_params.get('utm_term'),
                        'utmContent': self.filter_params.get('utm_content')
                    }],
                    'dot': self.filter_used
                }
            ],
            'search': {
                'placeholder': _('v_pipeline_header_search'),
                'onSearch': 'onSearchLeads'
            }
        }

        if not self.has_any_integration:
            header['actions'].append({
                '_com': 'Button',
                'type': 'solid',
                'icon': 'plusCircle',
                'label': _('v_pipeline_header_autoCreate'),
                'to': ['control', {
                    'tab': 'extensions',
                    'category': os.environ.get('AUTOCREATE_CATEGORY_ID')
                }]
            })

        return header

    def get_schema(self, params, request_data):
        board_columns = []

        for status in self.statuses:
            board_column_items = []

            for lead in status['leads']:
                lead_component = get_lead_component(lead,
                                                    installation_card_settings=self.installation_card_settings)
                board_column_items.append(lead_component)

            board_columns.append({
                'key': status['id'],
                'title': status['name'],
                'subtitle': self.installation_card_settings.format_amount(status['lead_amount_sum']) if self.installation_card_settings.amount_enabled else None,
                'color': get_hex_by_color(status['color']),
                'items': board_column_items,
                'showAdd': False if (
                            params.get('search') or self.filter_used) else True,
                'onAdd': 'addLead',
                'total': status['lead_count'],
                'loadLimit': 10,
                'onLoad': ['loadLeads', {
                    'statusId': status['id'],
                    'addToEnd': True
                }]
            })

        return [
            {
                '_com': 'Board',
                '_id': 'leadsBoard',
                'draggableBetweenColumns': True,
                'onDrag': 'onDragLead',
                'columns': board_columns
            }
        ]


# Get lead component
def get_lead_component(lead, installation_card_settings):
    title = ''
    description = []
    for field in lead['fields']:
        if field['value'] and field['field_value_type'] in ('string', 'number', 'date'):
            if field['field_board_visibility'] == 'title':
                title += field['value'] + ' '
            elif field['field_board_visibility'] == 'subtitle':
                description.append(field['value'])
    title = title.strip()

    extra = ['Archived' if lead['archived'] else Lead.get_regular_date(lead['add_date'])]
    if installation_card_settings.amount_enabled and lead['amount'] and lead['amount'] > 0:
        extra.insert(0, installation_card_settings.format_amount(lead['amount']))

    return {
        'key': lead['id'],
        'columnKey': lead['status_id'],
        'title': title if title else '#{}'.format(lead['uid']),
        'description': description if len(description) > 0 else None,
        'extra': extra,
        'order': lead['id'],
        'toWindow': ['updateLead', {
            'id': lead['id']
        }]
    }
