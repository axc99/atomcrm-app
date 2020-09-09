from flaskr import db
from flaskr.models.field import Field


# Create field
def create_field(params, request_data):
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


# Update field index
def update_field_index(params, request_data):
    fields = Field.query\
        .filter_by(veokit_installation_id=request_data['installation_id'])\
        .all()

    # TODO: update field indexes


# Delete field
def delete_field(params, request_data):
    if params.get('id'):
        Field.query \
            .filter_by(id=params.get('id')) \
            .delete()

        db.session.commit()