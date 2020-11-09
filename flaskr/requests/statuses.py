from cerberus import Validator

from flaskr import db
from flaskr.models.status import Status
from flaskr.models.lead import Lead


# Create status
def create_status(params, request_data):
    vld = Validator({
        'name': {'type': 'string', 'required': True},
        'color': {'type': 'string', 'required': True, 'allowed': ['red', 'pink', 'purple', 'blue', 'green', 'orange']}
    })
    is_valid = vld.validate(params)
    if not is_valid:
        return {'res': 'err', 'message': 'Invalid params', 'errors': vld.errors}

    new_status_index = Status.query \
                           .filter_by(nepkit_installation_id=request_data['installation_id']) \
                           .count() - 1

    new_status = Status()
    new_status.nepkit_installation_id = request_data['installation_id']
    new_status.name = params['name']
    new_status.color = params['color']
    new_status.index = new_status_index if new_status_index > 0 else 0

    db.session.add(new_status)
    db.session.commit()

    return {
        'res': 'ok',
        'status_id': 1
    }


# Update status
def update_status(params, request_data):
    vld = Validator({
        'id': {'type': 'number', 'required': True},
        'name': {'type': 'string', 'required': True},
        'color': {'type': 'string', 'required': True, 'allowed': ['red', 'pink', 'purple', 'blue', 'green', 'orange']}
    })
    is_valid = vld.validate(params)
    if not is_valid:
        return {'res': 'err', 'message': 'Invalid params', 'errors': vld.errors}

    status = Status.query \
        .filter_by(id=params['id']) \
        .first()

    status.name = params.get('name')
    status.color = params.get('color')

    db.session.commit()

    return {
        'res': 'ok'
    }


# Update status index
def update_status_index(params, request_data):
    vld = Validator({
        'id': {'type': 'number', 'required': True},
        'newIndex': {'type': 'number', 'required': True}
    })
    is_valid = vld.validate(params)
    if not is_valid:
        return {'res': 'err', 'message': 'Invalid params', 'errors': vld.errors}

    statuses = Status.query \
        .filter_by(nepkit_installation_id=request_data['installation_id']) \
        .order_by(Status.index.asc()) \
        .all()

    status_current_index = next((i for i, s in enumerate(statuses) if s.id == params['id']), None)

    statuses.insert(params['newIndex'], statuses.pop(status_current_index))

    i = 0
    for status in statuses:
        status.index = i
        i += 1
    db.session.commit()

    return {
        'res': 'ok'
    }


# Delete status
def delete_status(params, request_data):
    vld = Validator({
        'id': {'type': 'number', 'required': True},
        'assignedStatusId': {'type': 'number', 'nullable': True}
    })
    is_valid = vld.validate(params)
    if not is_valid:
        return {'res': 'err', 'message': 'Invalid params', 'errors': vld.errors}

    if params.get('assignedStatusId'):
        Lead.query \
            .filter_by(nepkit_installation_id=request_data['installation_id'],
                       status_id=params['id']) \
            .update({'status_id': params['assignedStatusId']})
    else:
        Lead.query \
            .filter_by(nepkit_installation_id=request_data['installation_id'],
                       status_id=params['id']) \
            .delete()

    Status.query \
        .filter_by(id=params['id'],
                   nepkit_installation_id=request_data['installation_id']) \
        .delete()

    db.session.commit()

    return {
        'res': 'ok'
    }
