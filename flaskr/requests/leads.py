from cerberus import Validator

from flaskr import db
from flaskr.models.lead import Lead
from flaskr.views.pipeline.pipeline import get_lead_component


# Get lead components for status
def get_lead_components(params, request_data):
    vld = Validator({
        'offset': {'type': 'number'},
        'limit': {'type': 'number'},
        'statusId': {'type': 'number', 'required': True},
        'search': {'type': 'string', 'empty': True}
    })
    is_valid = vld.validate(params)

    if not is_valid:
        return {'_res': 'err', 'message': 'Invalid params'}

    leads_q = db.session.execute("""  
        SELECT 
            l.*
        FROM 
            public.lead AS l
        WHERE
            l.veokit_installation_id = :installation_id AND 
            l.status_id = :status_id
        ORDER BY 
            l.add_date
        LIMIT
            :limit
        OFFSET
            :offset""", {
        'installation_id': request_data['installation_id'],
        'limit': params['limit'],
        'offset': params['offset'],
        'status_id': params['statusId']
    })

    lead_components = []
    for lead in leads_q:
        lead_components.append(get_lead_component({
            'id': lead.id,
            'status_id': lead.status_id,
            'fields': lead.get_fields(),
            'tags': lead.get_tags()
        }))

    return {
        '_res': 'ok',
        'leadComponents': lead_components,
        'leadTotal': 100
    }


# Create lead
def create_lead(params, request_data):
    vld = Validator({
        'statusId': {'type': 'number', 'required': True}
    })
    is_valid = vld.validate(params)

    if not is_valid:
        return {'_res': 'err', 'message': 'Invalid params'}

    # Create lead
    new_lead = Lead()
    new_lead.status_id = params['statusId']
    new_lead.veokit_installation_id = request_data['installation_id']

    db.session.add(new_lead)
    db.session.commit()

    return {
        '_res': 'ok',
        'leadId': new_lead.id
    }


# Update lead
def update_lead(params, request_data):
    vld = Validator({
        'id': {'type': 'number', 'required': True},
        'status_id': {'type': 'number', 'required': True},
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
                    'value': {'type': ['number', 'string', 'boolean', 'list'], 'required': True}
                }
            }
        }
    })
    is_valid = vld.validate(data)

    if not is_valid:
        return {'_res': 'err', 'message': 'Invalid params'}

    # Get lead by id
    lead = Lead.query \
        .filter_by(id=params['id'],
                   veokit_installation_id=request_data['installation_id']) \
        .first()
    if not lead:
        return {'_res': 'err', 'message': 'Unknown lead'}

    # Update lead
    lead.status_id = params['status_id']
    if data.get('archived') is not None:
        lead.archived = data['archived']

    db.session.commit()

    # Set tags and fields
    if data.get('tags'):
        lead.set_tags(data['tags'])
    if data.get('fields'):
        lead.set_fields(data['fields'])

    return {
        '_res': 'ok'
    }
