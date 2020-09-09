from flaskr.views.view import View
from flaskr.models.lead import Lead
from flaskr.models.field import Field
from flaskr.models.status import Status, StatusColor


# Window: Update lead
class UpdateLead(View):
    lead = None
    fields = []
    statuses = []

    def before(self, params, request_data):
        self.lead = Lead.query \
            .filter_by(id=params['id']) \
            .first()
        self.fields = Field.query \
            .filter_by(veokit_installation_id=request_data['installation_id']) \
            .order_by(Field.index) \
            .all()
        self.statuses = Status.query \
            .filter_by(veokit_installation_id=request_data['installation_id']) \
            .order_by(Status.index) \
            .all()

    def get_meta(self, params, request_data):
        return {
            'name': 'Lead #{}'.format(self.lead.id),
            'size': 'medium'
        }

    def get_header(self, params, request_data):
        return {
            'title': self.meta.get('name')
        }

    def get_schema(self, params, request_data):
        lead_fields = []

        for field in self.fields:
            field_component = {}

            if field.value_type.name == 'boolean':
                field_component = {
                    '_com': 'Field.Checkbox',
                    'columnWidth': 12,
                    'key': field.id,
                    'text': field.name
                }
            else:
                field_component = {
                    '_com': 'Field.Input',
                    'key': field.id,
                    'type': 'text',
                    'columnWidth': 12,
                    'label': field.name
                }

            lead_fields.append(field_component)

        lead_statuses = []
        for status in self.statuses:
            lead_statuses.append({
                'value': status.id,
                'label': status.name,
                'color': status.color.name
            })

        return [
            {
                '_com': 'Grid',
                'columns': [
                    {
                        'span': 7,
                        'content': [
                            {
                                '_com': 'Form',
                                '_id': 'createLeadForm',
                                'onFinish': 'onFinish',
                                'fields': lead_fields,
                                'buttons': [
                                    {
                                        '_com': 'Button',
                                        'type': 'primary',
                                        'submitForm': True,
                                        'icon': 'save',
                                        'label': 'Save'
                                    },
                                    {
                                        '_com': 'Button',
                                        'icon': 'delete'
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'span': 5,
                        'content': [
                            {
                                '_com': 'Field.Select',
                                '_id': 'createLeadForm_status',
                                'placeholder': 'Select status',
                                'value': lead_statuses[0]['value'],
                                'options': lead_statuses
                            },
                            {
                                '_com': 'Field.Input',
                                '_id': 'createLeadForm_tags',
                                'multiple': True,
                                'placeholder': 'Enter tags...'
                            },
                            {
                                '_com': 'Details',
                                'items': [
                                    { 'label': 'Add date', 'value': '25 Jun 2020 at 12:05' },
                                    { 'label': 'Update date', 'value': '25 Jun 2020 at 12:05' }
                                ]
                            },
                            {
                                '_com': 'Details',
                                'title': 'UTM marks',
                                'items': [
                                    { 'label': 'utm_source', 'value': 'google' },
                                    { 'label': 'utm_id', 'value': '23' }
                                ]
                            },
                            {
                                '_com': 'User',
                                'userId': 2
                            }
                        ]
                    }
                ]
            }
        ]

    methods = {
        'onFinish':
            """(app, params, event) => {
                const { values } = event

                const window = app.getView()
                const form = window.getCom('createLeadForm')
                const statusId = window.getCom('createLeadForm_status').getAttr('value')

                form.setAttr('loading', true)

                app
                    .sendReq('createLead', {
                        fields: values,
                        tags: values,
                        statusId
                    })
                    .then(result => {
                        form.setAttr('loading', false)

                        if (result._res == 'ok') {
                            // Reload parent page
                            app.getPage().reload()
                        }
                    })
            }"""
    }
