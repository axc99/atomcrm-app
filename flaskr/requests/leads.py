from datetime import datetime, timedelta

from cerberus import Validator
from flaskr import db
from flaskr.models.lead import Lead
from flaskr.models.status import Status
from flaskr.views.pipeline.pipeline import get_lead_component


# Get lead components for status
def get_lead_components(params, request_data):
    vld = Validator({
        'offset': {'type': 'number'},
        'limit': {'type': 'number'},
        'statusId': {'type': 'number', 'required': True},
        'search': {'type': 'string', 'empty': True},
        'periodFrom': {'type': 'string', 'empty': True},
        'periodTo': {'type': 'string', 'empty': True}
    })
    is_valid = vld.validate(params)
    if not is_valid:
        return {'res': 'err', 'message': 'Invalid params', 'errors': vld.errors}

    leads_q = Lead.get_with_filter(installation_id=request_data['installation_id'],
                                   status_id=params['statusId'],
                                   offset=params['offset'],
                                   limit=params['limit'],
                                   search=params.get('search'),
                                   period_from=params.get('periodFrom'),
                                   period_to=params.get('periodTo'))

    lead_components = []
    lead_total = 0
    for lead in leads_q:
        if lead_total == 0:
            lead_total = lead.total

        lead_components.append(get_lead_component({
            'id': lead.id,
            'status_id': lead.status_id,
            'archived': lead.archived,
            'add_date': (lead.add_date + timedelta(minutes=request_data['timezone_offset'])).strftime('%Y-%m-%d %H:%M:%S'),
            'fields': Lead.get_fields(lead.id),
            'tags': Lead.get_tags(lead.id)
        }))

    return {
        'res': 'ok',
        'leadComponents': lead_components,
        'leadTotal': lead_total
    }


# Create lead
def create_lead(params, request_data):
    vld = Validator({
        'statusId': {'type': 'number', 'required': True}
    })
    is_valid = vld.validate(params)
    if not is_valid:
        return {'res': 'err', 'message': 'Invalid params', 'errors': vld.errors}

    # Create lead
    new_lead = Lead()
    new_lead.status_id = params['statusId']
    new_lead.veokit_installation_id = request_data['installation_id']

    db.session.add(new_lead)
    db.session.commit()

    return {
        'res': 'ok',
        'leadId': new_lead.id
    }


# Update lead
def update_lead(params, request_data):
    vld = Validator({
        'id': {'type': 'number', 'required': True},
        'statusId': {'type': 'number', 'required': True},
        'archived': {'type': 'boolean'},
        'tags': {
            'type': 'list',
            'schema': {'type': ['number', 'string']}
        },
        'fields': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'fieldId': {'type': 'number', 'required': True, 'nullable': False},
                    'value': {'type': ['number', 'string', 'boolean', 'list'], 'required': True, 'nullable': True}
                }
            }
        }
    })
    is_valid = vld.validate(params)
    if not is_valid:
        return {'res': 'err', 'message': 'Invalid params', 'errors': vld.errors}

    # Get lead by id
    lead = Lead.query \
        .filter_by(id=params['id'],
                   veokit_installation_id=request_data['installation_id']) \
        .first()
    if not lead:
        return {'res': 'err', 'message': 'Unknown lead'}

    # Update lead
    lead.upd_date = datetime.utcnow()
    lead.status_id = params['statusId']
    if params.get('archived') is not None:
        lead.archived = params['archived']

    db.session.commit()

    # Set tags and fields
    if params.get('tags'):
        lead.set_tags(params['tags'])
    if params.get('fields'):
        lead.set_fields(params['fields'])

    return {
        'res': 'ok'
    }


# Upload lead status
def update_lead_status(params, request_data):
    vld = Validator({
        'id': {'type': 'number', 'required': True},
        'statusId': {'type': 'number', 'required': True}
    })
    is_valid = vld.validate(params)
    if not is_valid:
        return {'res': 'err', 'message': 'Invalid params', 'errors': vld.errors}

    lead = Lead.query \
        .filter_by(id=params['id']) \
        .first()
    lead.upd_date = datetime.utcnow()
    lead.status_id = params['statusId']

    db.session.commit()

    return {
        'res': 'ok'
    }


# Archive lead
def archive_lead(params, request_data):
    vld = Validator({
        'id': {'type': 'number', 'required': True}
    })
    is_valid = vld.validate(params)
    if not is_valid:
        return {'res': 'err', 'message': 'Invalid params', 'errors': vld.errors}

    lead = Lead.query \
        .filter_by(id=params['id']) \
        .first()
    lead.archived = True

    db.session.commit()

    return {
        'res': 'ok'
    }


# Restore lead
def restore_lead(params, request_data):
    vld = Validator({
        'id': {'type': 'number', 'required': True}
    })
    is_valid = vld.validate(params)
    if not is_valid:
        return {'res': 'err', 'message': 'Invalid params', 'errors': vld.errors}

    lead = Lead.query \
        .filter_by(id=params['id']) \
        .first()
    lead.archived = False

    db.session.commit()

    return {
        'res': 'ok'
    }
