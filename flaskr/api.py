from datetime import datetime

from flaskr.models.lead import Lead, LeadAction, LeadActionType
from flaskr.models.status import Status
from flaskr.models.field import Field
from flaskr import db
from cerberus import Validator


# Get leads
def get_leads(data, nepkit_installation_id):
    vld = Validator({
        'uid': {'type': ['string', 'list'], 'nullable': True}
    })
    is_valid = vld.validate(data)

    if not is_valid:
        return vld.errors, 400

    res_leads = []

    leads_q = Lead.query.filter_by(nepkit_installation_id=nepkit_installation_id)

    if data.get('uid'):
        if isinstance(data['uid'], list):
            leads_q = leads_q.filter(Lead.uid.in_(data['uid']))
        else:
            leads_q = leads_q.filter_by(uid=data['uid'])
    else:
        leads_q = leads_q.limit(500)

    leads = leads_q.all()

    for lead in leads:
        res_leads.append({
            'uid': lead.uid,
            'statusId': lead.status_id,
            'addDate': lead.add_date.strftime('%Y-%m-%d %H:%M:%S'),
            'updDate': lead.upd_date.strftime('%Y-%m-%d %H:%M:%S'),
            'fields': Lead.get_fields(lead.id, for_api=True),
            'tags': Lead.get_tags(lead.id, for_api=True)
        })

    return {
        'leads': res_leads
    }


# Create lead
def create_lead(data, nepkit_installation_id):
    vld = Validator({
        'statusId': {'type': 'number', 'required': True},
        'tags': {
            'type': 'list',
            'scheme': {'type': ['number', 'string']}
        },
        'fields': {
            'type': 'list',
            'scheme': {
                'type': 'dict',
                'scheme': {
                    'fieldId': {'type': 'number', 'required': True, 'nullable': False},
                    'value': {'type': ['number', 'string', 'boolean', 'list'], 'required': True}
                }
            }
        },
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

    return {
        'lead': {
            'uid': lead.uid,
            'statusId': lead.status_id,
            'addDate': lead.add_date.strftime('%Y-%m-%d %H:%M:%S'),
            'updDate': lead.upd_date.strftime('%Y-%m-%d %H:%M:%S'),
            'fields': Lead.get_fields(lead.id, for_api=True),
            'tags': Lead.get_tags(lead.id, for_api=True)
        }
    }


# Update lead
def update_lead(data, nepkit_installation_id):
    vld = Validator({
        'uid': {'type': 'string', 'required': True},
        'statusId': {'type': 'number', 'required': True},
        'tags': {
            'type': 'list',
            'scheme': {'type': ['number', 'string']}
        },
        'fields': {
            'type': 'list',
            'scheme': {
                'type': 'dict',
                'scheme': {
                    'fieldId': {'type': 'number', 'required': True, 'nullable': False},
                    'value': {'type': ['number', 'string', 'boolean', 'list'], 'required': True}
                }
            }
        }
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
        .filter_by(uid=data['uid'],
                   nepkit_installation_id=nepkit_installation_id) \
        .first()

    if not lead:
        return {"message": "Lead (uid={}) does not exist".format(data['uid'])}, 400

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
    db.session.commit()

    # Set tags and fields
    if data.get('tags'):
        lead.set_tags(data['tags'])
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
            'tags': Lead.get_tags(lead.id, for_api=True)
        }
    }


# Get statuses
def get_statuses(data, nepkit_installation_id):
    res_statuses = []

    statuses_q = Status.query.filter_by(nepkit_installation_id=nepkit_installation_id)

    if data.get('id'):
        if isinstance(data['id'], list):
            statuses_q = statuses_q.filter(Status.id.in_(data['id']))
        else:
            statuses_q = statuses_q.filter_by(id=data['id'])
    else:
        statuses_q = statuses_q.limit(500)

    statuses = statuses_q.all()

    for status in statuses:
        res_statuses.append({
            'id': status.id,
            'name': status.name
        })

    return {
        'statuses': res_statuses
    }


# Get fields
def get_fields(data, nepkit_installation_id):
    res_fields = []

    fields_q = Field.query.filter_by(nepkit_installation_id=nepkit_installation_id)

    if data.get('id'):
        if isinstance(data['id'], list):
            fields_q = fields_q.filter(Status.id.in_(data['id']))
        else:
            fields_q = fields_q.filter_by(id=data['id'])
    else:
        fields_q = fields_q.limit(500)

    fields = fields_q.all()

    for field in fields:
        res_fields.append({
            'id': field.id,
            'valueType': field.value_type.name,
            'name': field.name
        })

    return {
        'fields': res_fields
    }
