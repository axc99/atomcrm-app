from cerberus import Validator

from flaskr import db
from flaskr.models.lead import Lead


# Get leads
def get_leads(params, request_data):
    leads_q = Lead.query \
        .filter_by(veokit_installation_id=request_data['installation_id'],
                   status_id=params['statusId']) \
        .order_by(Lead.id.desc()) \
        .offset(0) \
        .limit(5) \
        .all()

    leads = []
    for lead in leads_q:
        leads.append({
            'id': lead.id,
            'title': lead.id,
            'description': lead.id
        })

    return {
        '_res': 'ok',
        'leads': leads,
        'total': 100
    }


# Create lead
def create_lead(params, request_data):
    vld = Validator({
        'statusId': {'type': 'number', 'required': True}
    })
    is_valid = vld.validate(params)

    # if not is_valid:
    #     return {'_res': 'err'}

    # Create lead
    new_lead = Lead()
    new_lead.status_id = params['statusId']
    new_lead.veokit_installation_id = request_data['installation_id']

    db.session.add(new_lead)
    db.session.commit()

    return {
        '_res': 'ok',
        'lead': {
            'title': 111,
            'description': 222
        },
        'leadId': None
    }


# Update lead
def update_lead(params, request_data):
    vld = Validator({
        'id': {'type': 'number', 'required': True},
        'status_id': {'type': 'number', 'required': True},
        'tags': {
            'type': 'list',
            'schema': {'type': ['number', 'string']}
        },
        'fields': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'field_id': {'type': 'number', 'required': True, 'nullable': False},
                    'value': {'type': ['number', 'string', 'boolean', 'list'], 'required': True}
                }
            }
        }
    })
    is_valid = vld.validate(data)

    if not is_valid:
        return {'_res': 'err'}

    # Get lead by id
    lead = Lead.query \
        .filter_by(id=params['id'],
                   veokit_installation_id=request_data['installation_id']) \
        .first()

    if not lead:
        return {'_res': 'err'}

    # Update lead
    lead.status_id = params['status_id']
    db.session.commit()

    # Set tags and fields
    if data.get('tags'):
        lead.set_tags(data['tags'])
    if data.get('fields'):
        lead.set_fields(data['fields'])

    return {
        '_res': 'ok'
    }


# Archive lead
def archive_lead(params, request_data):
    vld = Validator({
        'id': {'type': ['number', 'list'], 'nullable': True}
    })
    is_valid = vld.validate(data)

    if not is_valid:
        return {'_res': 'err'}

    # Get lead by id
    lead = Lead.query \
        .filter_by(id=params['id'],
                   veokit_installation_id=request_data['installation_id']) \
        .first()

    lead.archived = True
    db.session.commit()

    return {
        '_res': 'ok'
    }


# Restore lead
def restore_lead(params, request_data):
    vld = Validator({
        'id': {'type': ['number', 'list'], 'nullable': True}
    })
    is_valid = vld.validate(data)

    if not is_valid:
        return {'_res': 'err'}

    # Get lead by id
    lead = Lead.query \
        .filter_by(id=params['id'],
                   veokit_installation_id=request_data['installation_id']) \
        .first()

    lead.archived = False
    db.session.commit()

    return {
        '_res': 'ok'
    }
