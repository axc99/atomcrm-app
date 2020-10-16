from datetime import timedelta
from flask_babel import _

from cerberus import Validator

from flaskr.views.view import View
from flaskr.models.lead import Lead
from flaskr.models.field import Field
from flaskr.models.status import Status, StatusColor
from flaskr.models.installation_card_settings import InstallationCardSettings


# Window: Update lead
class UpdateLead(View):
    lead = None
    fields = []
    statuses = []

    def __init__(self):
        self.installation_card_settings = None

    def before(self, params, request_data):
        vld = Validator({
            'id': {'type': 'number', 'required': True}
        })
        is_valid = vld.validate(params)
        if not is_valid:
            raise Exception({'message': 'Invalid params',
                             'errors': vld.errors})

        self.installation_card_settings = InstallationCardSettings.query \
            .filter_by(veokit_installation_id=request_data['installation_id']) \
            .first()
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
            'name': _('v_updateLead_meta_name', id=self.lead.uid),
            'size': 'medium'
        }

    def get_header(self, params, request_data):
        return {
            'title': self.meta.get('name')
        }

    def get_schema(self, params, request_data):
        form_fields = []
        lead_fields = Lead.get_fields(self.lead.id)

        for field in self.fields:
            lead_field = next((f for f in lead_fields if f['field_id'] == field.id), None)
            field_value = lead_field['value'] if lead_field else None
            field_component = {}

            if field.value_type.name == 'boolean':
                field_component = {
                    '_com': 'Field.Checkbox',
                    'columnWidth': 12,
                    'key': field.id,
                    'text': field.name,
                    'value': field_value
                }
            elif field.value_type.name == 'long_string':
                field_component = {
                    '_com': 'Field.Input',
                    'columnWidth': 12,
                    'multiline': True,
                    'key': field.id,
                    'label': field.name,
                    'value': field_value
                }
            elif field.value_type.name == 'number':
                field_component = {
                    '_com': 'Field.Input',
                    'type': 'number',
                    'columnWidth': 6,
                    'key': field.id,
                    'label': field.name,
                    'value': field_value
                }
            elif field.value_type.name == 'date':
                field_component = {
                    '_com': 'Field.DatePicker',
                    'key': field.id,
                    'format': 'YYYY.MM.DD',
                    'label': field.name,
                    'value': field_value,
                    'allowClear': True
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

        currency = self.installation_card_settings.getCurrency()
        amount_prefix = currency['format_string'].split('{}')[0]
        amount_suffix = currency['format_string'].split('{}')[1]

        return [
            {
                '_com': 'Grid',
                'columns': [
                    {
                        'span': 12,
                        'sm': 7,
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
                                        'label': _('v_updateLead_save')
                                    },
                                    {
                                        '_com': 'Button',
                                        'icon': 'delete',
                                        'onClick': 'onClickArchive'
                                    } if not self.lead.archived else {
                                        '_com': 'Button',
                                        'icon': 'reload',
                                        'type': 'solid',
                                        'label': _('v_updateLead_restoreLead'),
                                        'onClick': 'onClickRestore'
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'span': 12,
                        'sm': 5,
                        'content': [
                            {
                                '_com': 'Area',
                                'background': '#f9f9f9',
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
                                        '_id': 'createLeadForm_amount',
                                        '_vis': self.installation_card_settings.amount_enabled,
                                        'type': 'number',
                                        'prefix': amount_prefix,
                                        'suffix': amount_suffix,
                                        'min': 0,
                                        'max': 10000000000,
                                        'placeholder': '0',
                                        'value': self.lead.amount
                                    },
                                    {
                                        '_com': 'Field.Input',
                                        '_id': 'createLeadForm_tags',
                                        'multiple': True,
                                        'value': Lead.get_tags(self.lead.id),
                                        'placeholder': _('v_updateLead_enterTags')
                                    },
                                    {
                                        '_com': 'Details',
                                        'items': [
                                            {
                                                'label': _('v_updateLead_addDate'),
                                                'value': Lead.get_regular_date((self.lead.add_date + timedelta(minutes=request_data['timezone_offset'])).strftime('%Y-%m-%d %H:%M:%S'))
                                            },
                                            {
                                                'label': _('v_updateLead_updateDate'),
                                                'value': Lead.get_regular_date((self.lead.upd_date + timedelta(minutes=request_data['timezone_offset'])).strftime('%Y-%m-%d %H:%M:%S'))
                                            },
                                            {
                                                'label': _('v_updateLead_creator'),
                                                'value': {
                                                    '_com': 'User',
                                                    'userId': self.lead.veokit_user_id
                                                }
                                            }
                                        ]
                                    },
                                    {
                                        '_com': 'Details',
                                        'title': _('v_updateLead_utmMarks'),
                                        'items': [
                                            {'label': 'utm_source', 'value': self.lead.utm_source} if self.lead.utm_source else None,
                                            {'label': 'utm_medium', 'value': self.lead.utm_medium} if self.lead.utm_medium else None,
                                            {'label': 'utm_campaign', 'value': self.lead.utm_campaign} if self.lead.utm_campaign else None,
                                            {'label': 'utm_term', 'value': self.lead.utm_term} if self.lead.utm_term else None,
                                            {'label': 'utm_content', 'value': self.lead.utm_content} if self.lead.utm_content else None
                                        ]
                                    } if (
                                        self.lead.utm_source or
                                        self.lead.utm_medium or
                                        self.lead.utm_campaign or
                                        self.lead.utm_term or
                                        self.lead.utm_content
                                    ) else None
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
                    const originalStatusId = """ + str(self.lead.status_id) + """
                    const amount = +window.getCom('createLeadForm_amount').getAttr('value')
                    const statusId = window.getCom('createLeadForm_status').getAttr('value')
                    const tags = window.getCom('createLeadForm_tags').getAttr('value')

                    const fields = []
                    Object.entries(values).map(([key, value]) => {
                        fields.push({
                            fieldId: +key,
                            value: value
                        })
                    })

                    form.setAttr('loading', true)

                    app
                        .sendReq('updateLead', {
                            id: """ + str(self.lead.id) + """,
                            amount,
                            fields,
                            tags,
                            statusId
                        })
                        .then(result => {
                            form.setAttr('loading', false)

                            if (result.res == 'ok') {
                                if (statusId != originalStatusId) {
                                    // Update status columns
                                    app.getPage().callMethod('loadLeads', { statusId: originalStatusId })  
                                    app.getPage().callMethod('loadLeads', { statusId })  
                                } else {
                                    // Update status column
                                    app.getPage().callMethod('loadLeads', { statusId: originalStatusId })  
                                } 
                                
                                window.close()
                            }
                        })
                }""",
            'onClickArchive':
                """(app, params, event) => {
                    app.openModal({
                        type: 'confirm',
                        title: '""" + _('v_updateLead_onClickArchive_title') + """',
                        text: '""" + _('v_updateLead_onClickArchive_text') + """',
                        okText: '""" + _('v_updateLead_onClickArchive_delete') + """',
                        onOk: modal => {
                            app
                                .sendReq('archiveLead', {
                                    id: """ + str(self.lead.id) + """
                                })
                                .then(result => {
                                    if (result.res == 'ok') {
                                        // Reload parent window
                                        app.getWindow().reload()
                                        
                                        // Reload leads on page
                                        app.getPage().callMethod('loadLeads', { statusId: """ + str(self.lead.status_id) + """ })
                                    }
                                })
                            }
                         })
                    }""",
            'onClickRestore':
                """(app, params, event) => {
                    app
                        .sendReq('restoreLead', {
                            id: """ + str(self.lead.id) + """
                        })
                        .then(result => {
                            if (result.res == 'ok') {
                                // Reload parent window
                                app.getWindow().reload()
                                
                                // Reload leads on page
                                app.getPage().callMethod('loadLeads', { statusId: """ + str(self.lead.status_id) + """ })
                            }
                        })     
                }"""
        }
