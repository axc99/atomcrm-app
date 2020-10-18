from flaskr.views.view import View
from flask_babel import _


# Window: Filter
class Filter(View):
    def __init__(self):
        self.meta = {
            'name': _('v_filter_meta_name')  # 'Filter'
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
                        'label': _('v_filter_schema_form_period'),  # 'Period',
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
                        'text': _('v_filter_schema_form_archivedLeads')  # 'Archived leads'
                    },
                ],
                'buttons': [
                    {
                        '_com': 'Button',
                        'icon': 'check',
                        'submitForm': True,
                        'type': 'primary',
                        'label': _('v_filter_schema_form_apply')  # 'Apply'
                    },
                    {
                        '_com': 'Button',
                        'label': _('v_filter_schema_form_clear'),  # 'Clear',
                        'onClick': 'onClickClear'
                    }
                ]
            }
        ]

    methods = {
        'onFinishForm': """(app, params, event) => {
            const { values } = event
             
            app
                .getPage()
                .to({
                    periodFrom: values.period ? values.period[0] : undefined,
                    periodTo: values.period ? values.period[1] : undefined,
                    archived: values.archived ? values.archived : undefined,
                    utmSource: values.utmSource,
                    utmMedium: values.utmMedium,
                    utmCampaign: values.utmCampaign,
                    utmTerm: values.utmTerm,
                    utmContent: values.utmContent
                })
        }""",
        'onClickClear': """(app, params, event) => {
            app
                .getPage()
                .to({})
        }"""
    }
