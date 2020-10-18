from datetime import datetime, timedelta

from cerberus import Validator
from flaskr import db
from flaskr.models.installation_card_settings import InstallationCardSettings
from flaskr.models.lead import Lead, LeadAction, LeadActionType
from flaskr.models.status import Status
from flaskr.views.pipeline.pipeline import get_lead_component


# Get lead components for status
def get_lead_components(params, request_data):
    installation_card_settings = InstallationCardSettings.query \
        .filter_by(veokit_installation_id=request_data['installation_id']) \
        .first()

    vld = Validator({
        'offset': {'type': 'number'},
        'limit': {'type': 'number'},
        'statusId': {'type': 'number', 'required': True},
        'search': {'type': 'string', 'empty': True},
        'filter': {'type': 'dict', 'required': False, 'nullable': True}
    })
    is_valid = vld.validate(params)
    if not is_valid:
        return {'res': 'err', 'message': 'Invalid params', 'errors': vld.errors}

    leads_q = Lead.get_with_filter(installation_id=request_data['installation_id'],
                                   status_id=params['statusId'],
                                   offset=params['offset'],
                                   limit=params['limit'],
                                   search=params.get('search'),
                                   filter=params.get('filter'))

    lead_components = []
    lead_total = 0
    lead_amount_sum = 0

    for lead in leads_q:
        if lead_total == 0:
            lead_total = lead.total
        if lead_amount_sum == 0:
            lead_amount_sum = lead.amount_sum

        lead_component = get_lead_component({
            'id': lead.id,
            'uid': lead.uid,
            'amount': lead.amount,
            'status_id': lead.status_id,
            'archived': lead.archived,
            'add_date': (lead.add_date + timedelta(minutes=request_data['timezone_offset'])).strftime('%Y-%m-%d %H:%M:%S'),
            'fields': Lead.get_fields(lead.id),
            'tags': Lead.get_tags(lead.id)
        }, installation_card_settings=installation_card_settings)
        lead_components.append(lead_component)

    return {
        'res': 'ok',
        'leadComponents': lead_components,
        'leadTotal': lead_total,
        'leadAmountSumStr': installation_card_settings.format_amount(lead_amount_sum) if installation_card_settings.amount_enabled else None
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
    new_lead.uid = Lead.get_uid()
    new_lead.status_id = params['statusId']
    new_lead.veokit_user_id = request_data['user_id']
    new_lead.veokit_installation_id = request_data['installation_id']
    db.session.add(new_lead)
    db.session.commit()

    # Log action
    new_action = LeadAction()
    new_action.type = LeadActionType.create_lead
    new_action.lead_id = new_lead.id
    new_action.new_status_id = new_lead.status_id
    new_action.veokit_user_id = request_data['user_id']
    db.session.add(new_action)
    db.session.commit()

    return {
        'res': 'ok',
        'leadId': new_lead.id
    }


# Update lead
def update_lead(params, request_data):
    vld = Validator({
        'id': {'type': 'number', 'required': True},
        'amount': {'type': 'number', 'required': False, 'nullable': True, 'min': 0},
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
                    'value': {'type': ['number', 'string', 'boolean', 'list'], 'required': False, 'nullable': True}
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

    old_status_id = lead.status_id

    # Update lead
    lead.upd_date = datetime.utcnow()
    lead.status_id = params['statusId']
    lead.amount = params['amount'] if params.get('amount') else 0
    if params.get('archived') is not None:
        lead.archived = params['archived']

    # Log action
    new_action = LeadAction()
    new_action.type = LeadActionType.update_lead
    new_action.lead_id = lead.id
    new_action.veokit_user_id = request_data['user_id']
    db.session.add(new_action)

    if old_status_id != lead.status_id:
        # Log change_status action
        new_action = LeadAction()
        new_action.type = LeadActionType.update_lead_status
        new_action.old_status_id = old_status_id
        new_action.new_status_id = lead.status_id
        new_action.lead_id = lead.id
        new_action.veokit_user_id = request_data['user_id']
        db.session.add(new_action)

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

    # Log action
    new_action = LeadAction()
    new_action.type = LeadActionType.archive_lead
    new_action.lead_id = lead.id
    new_action.veokit_user_id = request_data['user_id']
    db.session.add(new_action)

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

    # Log action
    new_action = LeadAction()
    new_action.type = LeadActionType.restore_lead
    new_action.lead_id = lead.id
    new_action.veokit_user_id = request_data['user_id']
    db.session.add(new_action)

    db.session.commit()

    return {
        'res': 'ok'
    }
