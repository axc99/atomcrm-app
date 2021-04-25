from datetime import datetime

from flaskr.models.installation_settings import InstallationSettings
from flaskr.models.lead import Lead, LeadAction, LeadActionType
from flaskr.models.status import Status
from flaskr.models.field import Field
from flaskr import db
from cerberus import Validator


# Get leads
def get_leads(resource_id, data, nepkit_installation_id):
    res_leads = []

    leads = Lead.query\
        .filter_by(nepkit_installation_id=nepkit_installation_id,
                                   uid=resource_id) \
        .all()

    for lead in leads:
        res_leads.append({
            'uid': lead.uid,
            'statusId': lead.status_id,
            'addDate': lead.add_date.strftime('%Y-%m-%d %H:%M:%S'),
            'updDate': lead.upd_date.strftime('%Y-%m-%d %H:%M:%S'),
            'fields': Lead.get_fields(lead.id, for_api=True),
            'tags': Lead.get_tags(lead.id, for_api=True),
            'completedTasks': Lead.get_completed_tasks(lead.id, for_api=True)
        })

    return {
        'leads': res_leads
    }


# Create lead
def create_lead(resource_id, data, nepkit_installation_id):
    vld = Validator({
        'statusId': {'type': 'number', 'required': True},
        'fields': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'fieldId': {'type': 'number', 'required': True, 'nullable': False},
                    'value': {'type': ['number', 'string', 'boolean', 'list'], 'required': True}
                }
            }
        },
        'tags': {
            'type': 'list',
            'schema': {'type': ['number', 'string']}
        },
        'completedTasks': {
            'type': 'list',
            'schema': {'type': ['number', 'string']}
        },
        'amount': {'type': ['number', 'string']},
        'utmSource': {'type': 'string'},
        'utmMedium': {'type': 'string'},
        'utmCampaign': {'type': 'string'},
        'utmTerm': {'type': 'string'},
        'utmContent': {'type': 'string'}
    })
    is_valid = vld.validate(data)

    if not is_valid:
        return vld.errors, 400

    # Parse fields
    fields = []
    for field in data['fields']:
        fields.append({
            'field_id': field['fieldId'],
            'value': field.get('value')
        })

    # Check status id
    is_status_exist = Status.query \
                          .filter_by(id=data['statusId'],
                                     nepkit_installation_id=nepkit_installation_id) \
                          .count() != 0
    if not is_status_exist:
        return {'message': 'Status (id={}) does not exist'.format(data['statusId'])}, \
               400

    # Create lead
    lead = Lead()
    lead.uid = Lead.get_uid()
    lead.nepkit_installation_id = nepkit_installation_id
    lead.status_id = data['statusId']
    lead.amount = data.get('amount', 0)
    lead.utm_source = data.get('utmSource', None)
    lead.utm_medium = data.get('utmMedium', None)
    lead.utm_campaign = data.get('utmCampaign', None)
    lead.utm_term = data.get('utmTerm', None)
    lead.utm_content = data.get('utmContent', None)

    db.session.add(lead)
    db.session.commit()

    # Add tags and fields
    if data.get('tags'):
        lead.set_tags(data['tags'], new_lead=True)
    if len(fields) > 0:
        lead.set_fields(fields, new_lead=True)

    # Log action
    new_action = LeadAction()
    new_action.type = LeadActionType.create_lead
    new_action.lead_id = lead.id
    new_action.new_status_id = lead.status_id
    db.session.add(new_action)
    db.session.commit()

    installation_settings = InstallationSettings.query \
        .filter_by(nepkit_installation_id=lead.nepkit_installation_id) \
        .first()
    if installation_settings.notifications_new_lead_extension_enabled:
        # Send notification
        fields_str = ''
        for field in Lead.get_fields(lead.id, for_api=True):
            fields_str += '{}: {} \r'.format(field['field_name'], field['value'])
        lead.send_notification(content={
            'en': 'New lead #{} \r{}'.format(lead.uid, fields_str),
            'ru': 'Новый лид #{} \r{}'.format(lead.uid, fields_str)
        })

    return {
        'lead': {
            'uid': lead.uid,
            'statusId': lead.status_id,
            'addDate': lead.add_date.strftime('%Y-%m-%d %H:%M:%S'),
            'updDate': lead.upd_date.strftime('%Y-%m-%d %H:%M:%S'),
            'fields': Lead.get_fields(lead.id, for_api=True),
            'tags': Lead.get_tags(lead.id, for_api=True),
            'completedTasks': []
        }
    }


# Update lead
def update_lead(resource_id, data, nepkit_installation_id):
    vld = Validator({
        'statusId': {'type': 'number', 'required': True},
        'fields': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'fieldId': {'type': 'number', 'required': True, 'nullable': False},
                    'value': {'type': ['number', 'string', 'boolean', 'list'], 'required': True}
                }
            }
        },
        'tags': {
            'type': 'list',
            'schema': {'type': ['number', 'string']}
        },
        'completedTasks': {
            'type': 'list',
            'schema': {'type': ['number', 'string']}
        },
        'amount': {'type': ['number', 'string']}
    })
    is_valid = vld.validate(data)

    if not is_valid:
        return vld.errors, 400

    # Parse fields
    fields = []
    for field in data['fields']:
        fields.append({
            'field_id': field['fieldId'],
            'value': field.get('value')
        })

    # Get lead by id
    lead = Lead.query \
        .filter_by(uid=resource_id,
                   nepkit_installation_id=nepkit_installation_id) \
        .first()

    if not lead:
        return {"message": "Lead (uid={}) does not exist".format(resource_id)}, 400

    if lead.status_id != data['statusId']:
        # Check status id
        is_status_exist = Status.query \
                              .filter_by(id=data['statusId'],
                                         nepkit_installation_id=nepkit_installation_id) \
                              .count() != 0
        if not is_status_exist:
            return {'message': 'Status (id={}) does not exist'.format(data['status_id'])}, \
                   400

    old_status_id = lead.status_id

    # Update lead
    lead.status_id = data['statusId']
    lead.upd_date = datetime.utcnow()
    lead.amount = data.get('amount', 0)
    db.session.commit()

    # Set tags, completed tasks and fields
    if 'tags' in data:
        lead.set_tags(data['tags'])
    if 'completedTasks' in data:
        lead.complete_tasks(data['completedTasks'])
    if len(fields) > 0:
        lead.set_fields(fields)

    # Log update action
    new_action = LeadAction()
    new_action.type = LeadActionType.update_lead
    new_action.lead_id = lead.id
    db.session.add(new_action)
    db.session.commit()

    if old_status_id != lead.status_id:
        # Log change_status action
        new_action = LeadAction()
        new_action.type = LeadActionType.update_lead_status
        new_action.old_status_id = old_status_id
        new_action.new_status_id = lead.status_id
        new_action.lead_id = lead.id
        db.session.add(new_action)
        db.session.commit()

    return {
        'lead': {
            'uid': lead.uid,
            'statusId': lead.status_id,
            'addDate': lead.add_date.strftime('%Y-%m-%d %H:%M:%S'),
            'updDate': lead.upd_date.strftime('%Y-%m-%d %H:%M:%S'),
            'fields': Lead.get_fields(lead.id, for_api=True),
            'tags': Lead.get_tags(lead.id, for_api=True),
            'completedTasks': Lead.get_completed_tasks(lead.id, for_api=True)
        }
    }
