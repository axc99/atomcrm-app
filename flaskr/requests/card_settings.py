from cerberus import Validator
from flaskr import db
from flaskr.models.field import Field
from flaskr.models.installation_settings import InstallationSettings


# Get fields
def get_fields(params, request_data):
    fields = []

    fields_q = Field.query \
        .filter_by(nepkit_installation_id=request_data['installation_id']) \
        .order_by(Field.index.asc()) \
        .all()
    for field in fields_q:
        fields.append({
            'id': field.id,
            'name': field.name,
            'valueType': field.value_type.name,
            'choiceOptions': field.choice_options,
            'boardVisibility': field.board_visibility.name
        })

    return {
        'res': 'ok',
        'fields': fields
    }


# Update card settings
def update_card_settings(params, request_data):
    vld = Validator({
        'amountEnabled': {'type': 'boolean', 'nullable': True},
        'currency': {'type': 'string', 'nullable': True},
        'fields': {'type': 'list', 'nullable': True},
        'notificationsNewLeadUserEnabled': {'type': 'boolean', 'nullable': True},
        'notificationsNewLeadExtensionEnabled': {'type': 'boolean', 'nullable': True},
        'notificationsNewLeadApiEnabled': {'type': 'boolean', 'nullable': True}
    })
    is_valid = vld.validate(params)
    if not is_valid:
        return {'res': 'err', 'message': 'Invalid params', 'errors': vld.errors}

    card_settings = InstallationSettings.query \
        .filter_by(nepkit_installation_id=request_data['installation_id']) \
        .first()

    if params.get('amountEnabled', None) is not None:
        card_settings.amount_enabled = params['amountEnabled']
    if params.get('currency', None) is not None:
        card_settings.currency = params['currency']

    if params.get('notificationsNewLeadUserEnabled', None) is not None:
        card_settings.notifications_new_lead_user_enabled = params['notificationsNewLeadUserEnabled']
    if params.get('notificationsNewLeadExtensionEnabled', None) is not None:
        card_settings.notifications_new_lead_extension_enabled = params['notificationsNewLeadExtensionEnabled']
    if params.get('notificationsNewLeadApiEnabled', None) is not None:
        card_settings.notifications_new_lead_api_enabled = params['notificationsNewLeadApiEnabled']

    # Set fields
    if params.get('fields'):
        i = 0
        removed_field_ids = []

        # Get current fields
        exist_fields = Field.query \
            .filter_by(nepkit_installation_id=request_data['installation_id']) \
            .order_by(Field.index.asc()) \
            .all()
        for exist_field in exist_fields:
            removed_field_ids.append(exist_field.id)

        for field in params['fields']:
            if field.get('name') and field.get('valueType'):
                if field.get('id'):
                    # Update exist field
                    exist_field = Field.query \
                        .filter_by(id=field['id'],
                                   nepkit_installation_id=request_data['installation_id']) \
                        .first()
                    exist_field.index = i
                    exist_field.name = field['name']
                    exist_field.value_type = field['valueType']
                    exist_field.choice_options = field['choiceOptions'] if field.get('choiceOptions') else None
                    exist_field.board_visibility = field['boardVisibility']

                    removed_field_ids.remove(exist_field.id)
                else:
                    # Create new field
                    new_field = Field()
                    new_field.index = i
                    new_field.name = field['name']
                    new_field.value_type = field['valueType']
                    new_field.choice_options = field['choiceOptions'] if field.get('choiceOptions') else None
                    new_field.board_visibility = field['boardVisibility']
                    new_field.nepkit_installation_id = request_data['installation_id']

                    db.session.add(new_field)
            i += 1

        if len(removed_field_ids) > 0:
            Field.query \
                .filter(Field.id.in_(removed_field_ids, )) \
                .delete(synchronize_session=False)

    db.session.commit()

    return {
        'res': 'ok'
    }
