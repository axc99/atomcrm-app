from flaskr import db
from flaskr.models.status import Status


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
        '_res': 'ok',
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
        '_res': 'ok'
    }


# Update status index
def update_status_index(params, request_data):
    statuses = Status.query\
        .filter_by(veokit_installation_id=request_data['installation_id'])\
        .all()

    # TODO: update status indexes


# Delete status
def delete_status(params, request_data):
    if params.get('id'):
        Status.query \
            .filter_by(id=params.get('id')) \
            .delete()

        db.session.commit()

    return {
        '_res': 'ok'
    }