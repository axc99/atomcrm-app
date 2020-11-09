from cerberus import Validator

from flaskr import db
from flaskr.models.task import Task, Task
from flaskr.models.lead import LeadCompletedTask


# Create tasks set
def create_task(params, request_data):
    vld = Validator({
        'name': {'type': 'string', 'required': True},
        'tasks': {'type': 'list', 'required': True}
    })
    is_valid = vld.validate(params)
    if not is_valid:
        return {'res': 'err', 'message': 'Invalid params', 'errors': vld.errors}

    new_set = Task()
    new_set.nepkit_installation_id = request_data['installation_id']
    new_set.name = params['name']
    new_set.index = Task.query \
                       .filter_by(nepkit_installation_id=request_data['installation_id']) \
                       .count() - 1

    db.session.add(new_set)
    db.session.commit()

    # Set tasks
    new_set.set_subtasks(params['tasks'])

    return {
        'res': 'ok',
        'status_id': 1
    }


# Update tasks set
def update_task(params, request_data):
    vld = Validator({
        'id': {'type': 'number', 'required': True},
        'name': {'type': 'string', 'required': True},
        'tasks': {'type': 'list', 'required': True}
    })
    is_valid = vld.validate(params)
    if not is_valid:
        return {'res': 'err', 'message': 'Invalid params', 'errors': vld.errors}

    task = Task.query \
        .filter_by(id=params['id']) \
        .first()

    task.name = params.get('name')

    db.session.commit()

    # Set tasks
    task.set_subtasks(params['tasks'])

    return {
        'res': 'ok'
    }


# Update tasks set index
def update_task_index(params, request_data):
    vld = Validator({
        'id': {'type': 'number', 'required': True},
        'newIndex': {'type': 'number', 'required': True}
    })
    is_valid = vld.validate(params)
    if not is_valid:
        return {'res': 'err', 'message': 'Invalid params', 'errors': vld.errors}

    tasks = Task.query \
        .filter_by(nepkit_installation_id=request_data['installation_id']) \
        .order_by(Task.index.asc()) \
        .all()

    task_current_index = next((i for i, s in enumerate(tasks) if s.id == params['id']), None)

    tasks.insert(params['newIndex'], tasks.pop(task_current_index))

    i = 0
    for task in tasks:
        task.index = i
        i += 1
    db.session.commit()

    return {
        'res': 'ok'
    }


# Delete tasks set
def delete_task(params, request_data):
    vld = Validator({
        'id': {'type': 'number', 'required': True}
    })
    is_valid = vld.validate(params)
    if not is_valid:
        return {'res': 'err', 'message': 'Invalid params', 'errors': vld.errors}

    task = Task.query \
            .filter_by(id=params['id'],
                       nepkit_installation_id=request_data['installation_id']) \
            .first()
    if not task:
        return {'res': 'err', 'message': 'Unknown tasks set'}

    # Delete lead tasks
    db.session.execute("""  
        DELETE FROM 
            public.lead_completed_task AS lct 
        WHERE 
            lct.task_id IN (
                SELECT 
                    t.id
                FROM
                    public.task AS t
                WHERE
                    t.id = :task_id
            )""", {
        'task_id': params['id']
    })
    Task.query \
        .filter_by(parent_task_id=params['id']) \
        .delete()

    db.session.delete(task)
    db.session.commit()

    return {
        'res': 'ok'
    }
