from flaskr.views.view import View, get_method
from flask_babel import _

compiled_methods = {
    'onFinishForm': get_method('methods/onFinishForm'),
    'onClickClear': get_method('methods/onClickClear')
}


# Window: Filter
class Filter(View):
    def __init__(self):
        self.meta = {
            'name': _('v_filter_meta_name')
        }
        self.data = {
            'filterParams': {
                'period': [filterParams['periodFrom'], filterParams['periodTo']],
                'utmSource': filterParams['utmSource'],
                'utmMedium': filterParams['utmMedium'],
                'utmCampaign': filterParams['utmCampaign'],
                'utmTerm': filterParams['utmTerm'],
                'utmContent': filterParams['utmContent'],
                'archived': filterParams['archived']
            },
            'strs': {
                'schema_form_period': _('v_filter_schema_form_period'),
                'schema_form_utmSource': _('v_filter_schema_form_utmSource'),
                'schema_form_utmMedium': _('v_filter_schema_form_utmMedium'),
                'schema_form_utmCampaign': _('v_filter_schema_form_utmCampaign'),
                'schema_form_utmTerm': _('v_filter_schema_form_utmTerm'),
                'schema_form_utmContent': _('v_filter_schema_form_utmContent'),
                'schema_form_archivedLeads': _('v_filter_schema_form_archivedLeads'),
                'schema_form_apply': _('v_filter_schema_form_apply'),
                'schema_form_clear': _('v_filter_schema_form_clear')
            }
        }

    def get_header(self, params, request_data):
        return {
            'title': self.meta.get('name')
        }

    def get_schema(self, params, request_data):
        return [
            {
                '_com': 'Form',
                'onFinish': 'onFinishForm',
                'fields': [
                    {
                        '_com': 'Field.DatePicker',
                        'key': 'period',
                        'label': _('v_filter_schema_form_period'),
                        'columnWidth': 12,
                        'range': True,
                        'allowClear': True,
                        'format': 'YYYY.MM.DD',
                        'value': [
                            params['periodFrom'] if params.get('periodFrom') else None,
                            params['periodTo'] if params.get('periodTo') else None
                        ]
                    },
                    {
                        '_com': 'Field.Input',
                        'key': 'utmSource',
                        'value': params.get('utmSource'),
                        'columnWidth': 6,
                        'label': 'UTM source'
                    },
                    {
                        '_com': 'Field.Input',
                        'key': 'utmMedium',
                        'value': params.get('utmMedium'),
                        'columnWidth': 6,
                        'label': 'UTM medium'
                    },
                    {
                        '_com': 'Field.Input',
                        'key': 'utmCampaign',
                        'value': params.get('utmCampaign'),
                        'columnWidth': 6,
                        'label': 'UTM campaign'
                    },
                    {
                        '_com': 'Field.Input',
                        'key': 'utmTerm',
                        'value': params.get('utmTerm'),
                        'columnWidth': 6,
                        'label': 'UTM term'
                    },
                    {
                        '_com': 'Field.Input',
                        'key': 'utmContent',
                        'value': params.get('utmContent'),
                        'columnWidth': 6,
                        'label': 'UTM content'
                    },
                    {
                        '_com': 'Field.Checkbox',
                        'key': 'archived',
                        'value': params.get('archived'),
                        'text': _('v_filter_schema_form_archivedLeads')
                    },
                ],
                'buttons': [
                    {
                        '_com': 'Button',
                        'icon': 'check',
                        'submitForm': True,
                        'type': 'primary',
                        'label': _('v_filter_schema_form_apply')
                    },
                    {
                        '_com': 'Button',
                        'label': _('v_filter_schema_form_clear'),
                        'onClick': 'onClickClear'
                    }
                ]
            }
        ]

    methods = compiled_methods
