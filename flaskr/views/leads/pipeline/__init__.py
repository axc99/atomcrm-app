import os
from datetime import timedelta
from flask_babel import _
import json

from flaskr import db
from flaskr.models.installation_extension_settings import InstallationExtensionSettings
from flaskr.views.view import View, get_method, method_with_vars
from flaskr.models.lead import Lead
from flaskr.models.status import Status, get_hex_by_color
from flaskr.models.installation_card_settings import InstallationCardSettings

compiled_methods = {
    'addLead': get_method('methods/addLead'),
    'loadLeads': get_method('methods/loadLeads'),
    'onDragLead': get_method('methods/onDragLead'),
    'onSearchLeads': get_method('methods/onSearchLeads')
}


# Page: Pipeline
class Pipeline(View):
    def __init__(self):
        self.leads = []
        self.statuses = []
        self.meta = {
            'name': _('v_pipeline_meta_name')
        }
        self.installation_card_settings = None
        self.filter_used = False
        self.filter_params = {}
        self.has_any_integration = False

    def before(self, params, request_data):
        self.installation_card_settings = InstallationCardSettings.query \
            .filter_by(nepkit_installation_id=request_data['installation_id']) \
            .first()

        self.filter_params = {
            'period_from': params['periodFrom'].replace('.', '-') if params.get('periodFrom') else None,
            'period_to': params['periodTo'].replace('.', '-') if params.get('periodTo') else None,
            'archived': True if params.get('archived') == 'true' else False,
            'utm_source': params['utmSource'] if params.get('utmSource') else None,
            'utm_medium': params['utmMedium'] if params.get('utmMedium') else None,
            'utm_campaign': params['utmCampaign'] if params.get('utmCampaign') else None,
            'utm_term': params['utmTerm'] if params.get('utmTerm') else None,
            'utm_content': params['utmContent'] if params.get('utmContent') else None,
        }
        self.filter_used = any(self.filter_params.values())

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
            'amount_enabled': self.installation_card_settings.amount_enabled
        })

        self.has_any_integration = InstallationExtensionSettings.query \
            .filter_by(nepkit_installation_id=request_data['installation_id']) \
            .count() > 0


        self.statuses = []
        for status in statuses_q:
            leads_q = Lead.get_with_filter(installation_id=request_data['installation_id'],
                                           status_id=status['id'],
                                           search=params.get('search'),
                                           offset=0,
                                           limit=10,
                                           filter=self.filter_params)

            status_leads = []
            status_lead_total = 0
            status_lead_amount_sum = 0

            for lead in leads_q:
                if status_lead_total == 0:
                    status_lead_total = lead.total
                if status_lead_amount_sum == 0:
                    status_lead_amount_sum = lead.amount_sum

                status_leads.append({
                    'id': lead.id,
                    'uid': lead.uid,
                    'status_id': lead.status_id,
                    'amount': lead.amount,
                    'archived': lead.archived,
                    'add_date': (lead.add_date + timedelta(minutes=request_data['timezone_offset'])).strftime('%Y-%m-%d %H:%M:%S'),
                    'fields': Lead.get_fields(lead.id),
                    'tags': Lead.get_tags(lead.id)
                })

            self.statuses.append({
                'id': status['id'],
                'name': status['name'],
                'lead_count': status_lead_total,
                'lead_amount_sum': status_lead_amount_sum,
                'color': status['color'],
                'leads': status_leads
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

    def get_methods(self, params, request_data):
        methods = compiled_methods.copy()

        methods['addLead'] = method_with_vars(methods['addLead'], {'SEARCH': params['search'] if params.get('search') else '',
                                                                   'FILTER': json.dumps(self.filter_params)})
        methods['loadLeads'] = method_with_vars(methods['loadLeads'], {'SEARCH': params['search'] if params.get('search') else '',
                                                                       'FILTER': json.dumps(self.filter_params)})

        return methods


# Get lead component
def get_lead_component(lead, installation_card_settings):
    title = ''
    description = []
    for field in lead['fields']:
        if field['value']:
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
