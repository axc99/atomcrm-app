from cerberus import Validator
from flaskr import db
from flaskr.models.field import Field


# Create field
def create_field(params, request_data):
    vld = Validator({
        'name': {'type': 'string', 'required': True},
        'valueType': {'type': 'string', 'required': True},
        'min': {'type': 'number', 'min': 0, 'required': True},
        'max': {'type': 'number', 'max': 1000, 'required': True},
        'asTitle': {'type': 'boolean', 'required': True},
        'primary': {'type': 'boolean', 'required': True}
    })
    vld.allow_unknown = True
    is_valid = vld.validate(params)

    if not is_valid:
        return {'res': 'err', 'message': 'Invalid params', 'errors': vld.errors}

    new_field = Field()
    new_field.veokit_installation_id = request_data['installation_id']
    new_field.name = params.get('name')
    new_field.value_type = params.get('valueType')
    new_field.min = params.get('min')
    new_field.max = params.get('max')
    new_field.as_title = params.get('asTitle')
    new_field.primary = params.get('primary')
    new_field.index = Field.query\
                           .filter_by(veokit_installation_id = request_data['installation_id'])\
                           .count() - 1

    db.session.add(new_field)
    db.session.commit()

    return {
        'res': 'ok',
        'status_id': 1
    }


# Update field
def update_field(params, request_data):
    field = Field.query \
        .filter_by(id=params['id']) \
        .first()

    field.name = params.get('name')
    field.value_type = params.get('valueType')
    field.min = params.get('min')
    field.max = params.get('max')
    field.as_title = params.get('asTitle')
    field.primary = params.get('primary')

    db.session.commit()

    return {
        'res': 'ok'
    }


# Update field index
def update_field_index(params, request_data):
    fields = Field.query \
        .filter_by(veokit_installation_id=request_data['installation_id']) \
        .order_by(Field.index.asc()) \
        .all()

    field_current_index = next((i for i, s in enumerate(fields) if s.id == params['id']), None)

    fields.insert(params['newIndex'], fields.pop(field_current_index))

    i = 0
    for field in fields:
        field.index = i
        i += 1
    db.session.commit()

    return {
        'res': 'ok'
    }


# Delete field
def delete_field(params, request_data):
    if params.get('id'):
        Field.query \
            .filter_by(id=params.get('id')) \
            .delete()

        db.session.commit()

    return {
        'res': 'ok'
    }
