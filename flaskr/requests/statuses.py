from flaskr import db
from flaskr.models.status import Status
from flaskr.models.lead import Lead


# Create status
def create_status(params, request_data):
    new_status = Status()
    new_status.veokit_installation_id = request_data['installation_id']
    new_status.name = params.get('name')
    new_status.color = params.get('color')
    new_status.index = Status.query\
                           .filter_by(veokit_installation_id = request_data['installation_id'])\
                           .count() - 1

    db.session.add(new_status)
    db.session.commit()

    return {
        'res': 'ok',
        'status_id': 1
    }


# Update status
def update_status(params, request_data):
    status = Status.query\
        .filter_by(id=params['id'])\
        .first()

    status.name = params.get('name')
    status.color = params.get('color')

    db.session.commit()

    return {
        'res': 'ok'
    }


# Update status index
def update_status_index(params, request_data):
    statuses = Status.query\
        .filter_by(veokit_installation_id=request_data['installation_id'])\
        .order_by(Status.index.asc())\
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
    if params.get('assignedStatusId'):
        Lead.query \
            .filter_by(veokit_installation_id=request_data['installation_id'],
                       status_id=params['id']) \
            .update({'status_id': params['assignedStatusId']})
    else:
        Lead.query\
            .filter_by(veokit_installation_id=request_data['installation_id'],
                       status_id=params['id'])\
            .delete()

    Status.query \
        .filter_by(id=params['id']) \
        .delete()

    db.session.commit()

    return {
        'res': 'ok'
    }