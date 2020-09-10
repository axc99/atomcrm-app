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
            .filter_by(veokit_installation_id=request_data['installation_id'],
                       lead_id=self.lead.id) \
            .order_by(Field.index) \
            .all()
        self.statuses = Status.query \
            .filter_by(veokit_installation_id=request_data['installation_id'],
                       lead_id=self.lead.id) \
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
        form_fields = []
        lead_fields = self.lead.get_fields()

        for field in self.fields:
            field_value = [f for f in lead_fields if f['field_id'] == field.id],
            field_component = {}

            if field.value_type.name == 'boolean':
                field_component = {
                    '_com': 'Field.Checkbox',
                    'columnWidth': 12,
                    'key': field.id,
                    'text': field.name,
                    'value': field_value
                }
            else:
                field_component = {
                    '_com': 'Field.Input',
                    'key': field.id,
                    'type': 'text',
                    'columnWidth': 12,
                    'label': field.name,
                    'value': field_value
                }

            form_fields.append(field_component)

        status_options = []
        for status in self.statuses:
            status_options.append({
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
                                'fields': form_fields,
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
                                        'icon': 'delete',
                                        'type': 'danger',
                                        'onClick': 'onClickArchive'
                                    } if not self.lead.archived else {
                                        '_com': 'Button',
                                        'icon': 'reload',
                                        'type': 'solid',
                                        'label': 'Restore lead',
                                        'onClick': 'onClickRestore'
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'span': 5,
                        'content': [
                            {
                                '_com': 'Area',
                                'background': '#f5f5f5',
                                'content': [
                                    {
                                        '_com': 'Field.Select',
                                        '_id': 'createLeadForm_status',
                                        'placeholder': 'Select status',
                                        'value': self.lead.status_id,
                                        'options': status_options
                                    },
                                    {
                                        '_com': 'Field.Input',
                                        '_id': 'createLeadForm_tags',
                                        'multiple': True,
                                        'label': 'Tags',
                                        'value': lead.get_tags(),
                                        'placeholder': 'Enter tags'
                                    },
                                    {
                                        '_com': 'Details',
                                        'items': [
                                            {'label': 'Add date', 'value': self.lead.add_date.strftime('%d.%m.%Y at %H:%M')},
                                            {'label': 'Update date', 'value': self.lead.upd_date.strftime('%d.%m.%Y at %H:%M')},
                                            {
                                                'label': 'Creator',
                                                'value': {
                                                    '_com': 'User',
                                                    'userId': 2
                                                }
                                            }
                                        ]
                                    },
                                    {
                                        '_com': 'Details',
                                        'title': 'UTM marks',
                                        'items': [
                                            {'label': 'utm_source', 'value': self.lead.utm_source},
                                            {'label': 'utm_medium', 'value': self.lead.utm_medium},
                                            {'label': 'utm_campaign', 'value': self.lead.utm_campaign},
                                            {'label': 'utm_term', 'value': self.lead.utm_term},
                                            {'label': 'utm_content', 'value': self.lead.utm_content}
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]

    def get_methods(self, params, request_data):
        return {
            'onFinish':
                """(app, params, event) => {
                    const { values } = event

                    const window = app.getView()
                    const form = window.getCom('createLeadForm')
                    const statusId = window.getCom('createLeadForm_status').getAttr('value')

                    const fields = []
                    Object.entries(values).map(([key, value]) => {
                        fields.append({
                            fieldId: key,
                            value
                        })
                    })

                    form.setAttr('loading', true)

                    app
                        .sendReq('updateLead', {
                            fields,
                            tags: [],
                            statusId
                        })
                        .then(result => {
                            form.setAttr('loading', false)

                            if (result._res == 'ok') {
                                // Reload parent page
                                app.getPage().reload()
                            }
                        })
                }""",
            'onClickArchive':
                """(app, params, event) => {
                     app.openModal({
                        type: 'answer',
                        title: 'Delete lead?',
                        content: 'Are you sure you want to move this lead to the archive? You can restore it at any time.',
                        okText: 'Delete',
                        onOk: modal => {
                            app
                                .sendReq('updateLead', {
                                    id: """ + self.lead.id + """,
                                    archived: true
                                })
                                .then(result => {
                                    if (result._res == 'ok') {
                                        // Reload parent page
                                        app.getWindow().reload()
                                    }
                                })
                            }
                         })
                    }""",
            'onClickRestore':
                """(app, params, event) => {
                    app
                        .sendReq('updateLead', {
                            id: """ + self.lead.id + """,
                            archived: false
                        })
                        .then(result => {
                            if (result._res == 'ok') {
                                // Reload parent page
                                app.getWindow().reload()
                            }
                        })     
                }"""
        }
