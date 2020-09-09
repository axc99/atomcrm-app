from flaskr.models.lead import Lead, LeadTag
from flaskr.models.status import Status
from flaskr.models.field import Field
from flaskr.models.tag import Tag
from flaskr import db
from cerberus import Validator


# Get leads
def get_leads(data, veokit_installation_id):
    vld = Validator({
        'id': {'type': ['number', 'list'], 'nullable': True}
    })
    is_valid = vld.validate(data)

    if not is_valid:
        return vld.errors, 400

    res_leads = []

    leads_q = Lead.query.filter_by(veokit_installation_id=veokit_installation_id)

    if data.get('id'):
        if isinstance(data['id'], list):
            leads_q = leads_q.filter(Lead.id.in_(data['id']))
        else:
            leads_q = leads_q.filter_by(id=data['id'])
    else:
        leads_q = leads_q.limit(500)

    leads = leads_q.all()

    for lead in leads:
        res_leads.append({
            'id': lead.id,
            'status_id': lead.status_id,
            'add_date': lead.add_date.strftime('%Y-%m-%d %H:%M:%S'),
            'upd_date': lead.upd_date.strftime('%Y-%m-%d %H:%M:%S'),
            'fields': lead.get_fields(for_api=True),
            'tags': lead.get_tags(for_api=True)
        })

    return {
        'leads': res_leads
    }


# Create lead
def create_lead(data, veokit_installation_id):
    vld = Validator({
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
        return vld.errors, 400

    # Check status id
    is_status_exist = Status.query \
                          .filter_by(id=data['status_id'],
                                     veokit_installation_id=veokit_installation_id) \
                          .count() != 0
    if not is_status_exist:
        return {'message': 'Status (id={}) does not exist'.format(data['status_id'])}, \
               400

    # Create lead
    lead = Lead()
    lead.veokit_installation_id = veokit_installation_id
    lead.status_id = data['status_id']
    db.session.add(lead)
    db.session.commit()

    # Add tags and fields
    if data.get('tags'):
        lead.set_tags(data['tags'], new_lead=True)
    if data.get('fields'):
        lead.set_fields(data['fields'], new_lead=True)

    return {
        'lead': {
            'id': lead.id,
            'status_id': lead.status_id,
            'add_date': lead.add_date.strftime('%Y-%m-%d %H:%M:%S'),
            'upd_date': lead.upd_date.strftime('%Y-%m-%d %H:%M:%S'),
            'fields': lead.get_fields(for_api=True),
            'tags': lead.get_tags(for_api=True)
        }
    }


# Update lead
def update_lead(data, veokit_installation_id):
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
        return vld.errors, 400

    # Get lead by id
    lead = Lead.query \
        .filter_by(id=data['id'],
                   veokit_installation_id=veokit_installation_id) \
        .first()

    if not lead:
        return {"message": "Lead (id={}) does not exist".format(data['id'])}, 400

    if lead.status_id != data['status_id']:
        # Check status id
        is_status_exist = Status.query \
                              .filter_by(id=data['status_id'],
                                         veokit_installation_id=veokit_installation_id) \
                              .count() != 0
        if not is_status_exist:
            return {'message': 'Status (id={}) does not exist'.format(data['status_id'])}, \
                   400

    # Update lead
    lead.status_id = data['status_id']
    db.session.commit()

    # Set tags and fields
    if data.get('tags'):
        lead.set_tags(data['tags'])
    if data.get('fields'):
        lead.set_fields(data['fields'])

    return {
        'lead': {
            'id': lead.id,
            'status_id': lead.status_id,
            'add_date': lead.add_date.strftime('%Y-%m-%d %H:%M:%S'),
            'upd_date': lead.upd_date.strftime('%Y-%m-%d %H:%M:%S'),
            'fields': lead.get_fields(for_api=True),
            'tags': lead.get_tags(for_api=True)
        }
    }


# Get statuses
def get_statuses(data, veokit_installation_id):
    res_statuses = []

    statuses_q = Status.query.filter_by(veokit_installation_id=veokit_installation_id)

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
def get_fields(data, veokit_installation_id):
    res_fields = []

    fields_q = Field.query.filter_by(veokit_installation_id=veokit_installation_id)

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
            'value_type': field.value_type.name,
            'name': field.name,
            'min': field.min,
            'max': field.max
        })

    return {
        'fields': res_fields
    }
