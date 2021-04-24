from datetime import datetime, timedelta

from cerberus import Validator
from flaskr import db
from flaskr.models.field import Field
from flaskr.models.installation_settings import InstallationSettings
from flaskr.models.lead import Lead, LeadAction, LeadActionType
from flaskr.models.status import Status
from flaskr.models.task import Task


# Get leads
def get_leads(params, request_data):
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

    installation_settings = InstallationSettings.query \
        .filter_by(nepkit_installation_id=request_data['installation_id']) \
        .first()

    search = params['search']
    filter = {
        'period_from': params['filter']['periodFrom'],
        'period_to': params['filter']['periodTo'],
        'utm_source': params['filter']['utmSource'],
        'utm_medium': params['filter']['utmMedium'],
        'utm_campaign': params['filter']['utmCampaign'],
        'utm_term': params['filter']['utmTerm'],
        'utm_content': params['filter']['utmContent'],
        'archived': params['filter']['archived']
    }

    leads_q = Lead.get_with_filter(installation_id=request_data['installation_id'],
                                   status_id=params['statusId'],
                                   offset=params['offset'],
                                   limit=params['limit'],
                                   search=search,
                                   filter=filter)

    fields_q = Field.query \
        .filter_by(nepkit_installation_id=request_data['installation_id']) \
        .order_by(Field.index) \
        .all()

    leads = []
    lead_total = 0
    lead_amount_sum = 0

    for lead in leads_q:
        if lead_total == 0:
            lead_total = lead.total
        if lead_amount_sum == 0:
            lead_amount_sum = lead.amount_sum

        fields = []
        lead_fields = Lead.get_fields(lead.id)
        for field in fields_q:
            lead_field = next((f for f in lead_fields if f['field_id'] == field.id), None)
            field_value = lead_field['value'] if lead_field else None

            if field_value:
                fields.append({
                    'fieldId': field.id,
                    'fieldName': field.name,
                    'fieldValueType': field.value_type.name,
                    'fieldBoardVisibility': field.board_visibility.name,
                    'value': field_value
                })

        leads.append({
            'id': lead.id,
            'uid': lead.uid,
            'amount': lead.amount,
            'amountStr': installation_settings.format_amount(lead.amount) if lead.amount else None,
            'status_id': lead.status_id,
            'archived': lead.archived,
            'addDate': (lead.add_date + timedelta(minutes=request_data['timezone_offset'])).strftime('%Y-%m-%d %H:%M:%S'),
            'fields': fields
        })

    return {
        'res': 'ok',
        'leads': leads,
        'leadTotal': lead_total,
        'leadAmountSum': lead_amount_sum,
        'leadAmountSumStr': installation_settings.format_amount(lead_amount_sum) if installation_settings.amount_enabled else None
    }


# Get lead
def get_lead(params, request_data):
    vld = Validator({
        'id': {'type': 'number', 'required': True}
    })
    is_valid = vld.validate(params)
    if not is_valid:
        return {'res': 'err', 'message': 'Invalid params', 'errors': vld.errors}

    lead = Lead.query \
        .filter_by(id=params['id']) \
        .first()
    task_count = Task.query \
        .filter_by(nepkit_installation_id=request_data['installation_id']) \
        .count()

    fields = []
    fields_q = Field.query \
        .filter_by(nepkit_installation_id=request_data['installation_id']) \
        .order_by(Field.index) \
        .all()
    lead_fields = Lead.get_fields(lead.id)
    for field in fields_q:
        lead_field = next((f for f in lead_fields if f['field_id'] == field.id), None)
        field_value = lead_field['value'] if lead_field else None

        fields.append({
            'fieldId': field.id,
            'fieldName': field.name,
            'fieldValueType': field.value_type.name,
            'value': field_value,
            'choiceOptions': field.choice_options
        })
    tags = Lead.get_tags(lead.id)

    tasks = []
    tasks_q = db.session.execute("""
        SELECT
            t.*,
            (
                CASE
                    WHEN :lead_id is not NULL THEN (SELECT COUNT(*) FROM public.lead_completed_task as lct WHERE lct.task_id = t.id AND lct.lead_id = :lead_id) != 0
                    ELSE false
                END
            ) AS completed,
            (SELECT lct.add_date FROM public.lead_completed_task as lct WHERE lct.task_id = t.id AND lct.lead_id = :lead_id) AS complete_date
        FROM
            public.task AS t
        WHERE
            t.parent_task_id is null AND
            t.nepkit_installation_id = :nepkit_installation_id
        ORDER BY
            t.index""", {
        'nepkit_installation_id': request_data['installation_id'],
        'lead_id': lead.id
    })
    for task in tasks_q:
        tasks.append({
            'id': task.id,
            'name': task.name,
            'completed': task.completed,
            'completeDate': (task.complete_date + timedelta(minutes=request_data['timezone_offset'])).strftime('%Y-%m-%d %H:%M:%S') if task.complete_date else None
        })

    return {
        'res': 'ok',
        'lead': {
            'id': lead.id,
            'uid': lead.uid,
            'comment': lead.comment,
            'amount': lead.amount,
            'statusId': lead.status_id,
            'addDate': (lead.add_date + timedelta(minutes=request_data['timezone_offset'])).strftime('%Y-%m-%d %H:%M:%S'),
            'updDate': (lead.upd_date + timedelta(minutes=request_data['timezone_offset'])).strftime('%Y-%m-%d %H:%M:%S'),
            'nepkitUserId': lead.nepkit_user_id,
            'utmSource': lead.utm_source,
            'utmMedium': lead.utm_medium,
            'utmCampaign': lead.utm_campaign,
            'utmTerm': lead.utm_term,
            'utmContent': lead.utm_content,
            'taskCount': task_count,
            'fields': fields,
            'tags': tags,
            'tasks': tasks
        }
    }


# Get lead actions
def get_lead_actions(params, request_data):
    vld = Validator({
        'leadId': {'type': 'number', 'required': True},
        'limit': {'type': 'number'},
        'offset': {'type': 'number'}
    })
    is_valid = vld.validate(params)
    if not is_valid:
        return {'res': 'err', 'message': 'Invalid params', 'errors': vld.errors}

    actions = []
    actions_q = db.session.execute("""
        SELECT
            la.*,
            old_s.name AS old_status_name,
            new_s.name AS new_status_name,
            comp_t.name AS task_name,
            COUNT(*) OVER () AS total
        FROM
            public.lead_action AS la
        LEFT JOIN 
            public.status AS old_s ON old_s.id = la.old_status_id
        LEFT JOIN  
            public.status AS new_s ON new_s.id = la.new_status_id
        LEFT JOIN  
            public.task AS comp_t ON comp_t.id = la.completed_task_id
        WHERE
            la.lead_id = :lead_id
        ORDER BY 
            la.log_date DESC
        LIMIT :limit OFFSET :offset""", {
        'lead_id': params['leadId'],
        'offset': params['offset'],
        'limit': params['limit']
    })

    action_total = 0
    for action in actions_q:
        if action_total == 0:
            action_total = action.total

        action_data = LeadAction.get_color_and_title(action)
        actions.append({
            'title': action_data['title'],
            'color': action_data['color'],
            'log_date': Lead.get_regular_date((action.log_date + timedelta(minutes=request_data['timezone_offset'])).strftime('%Y-%m-%d %H:%M:%S'))
        })

    return {
        'res': 'ok',
        'actions': actions,
        'actionTotal': action_total
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
    new_lead.nepkit_user_id = request_data['user_id']
    new_lead.nepkit_installation_id = request_data['installation_id']
    db.session.add(new_lead)
    db.session.commit()

    # Log action
    new_action = LeadAction()
    new_action.type = LeadActionType.create_lead
    new_action.lead_id = new_lead.id
    new_action.new_status_id = new_lead.status_id
    new_action.nepkit_user_id = request_data['user_id']
    db.session.add(new_action)
    db.session.commit()

    installation_settings = InstallationSettings.query \
        .filter_by(nepkit_installation_id=request_data['installation_id']) \
        .first()
    if installation_settings.notifications_new_lead_user_enabled:
        # Send notification
        new_lead.send_notification(content={
            'en': 'Added new lead #{}'.format(new_lead.uid),
            'ru': 'Добавлен новый лид #{}'.format(new_lead.uid)
        })

    return {
        'res': 'ok',
        'leadId': new_lead.id
    }


# Update lead
def update_lead(params, request_data):
    vld = Validator({
        'id': {'type': 'number', 'required': True},
        'amount': {'type': 'number', 'required': False, 'nullable': True, 'min': 0},
        'comment': {'type': 'string', 'required': False, 'nullable': True},
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

    # Parse fields
    fields = []
    for field in params['fields']:
        fields.append({
            'field_id': field['fieldId'],
            'value': field.get('value')
        })

    # Get lead by id
    lead = Lead.query \
        .filter_by(id=params['id'],
                   nepkit_installation_id=request_data['installation_id']) \
        .first()
    if not lead:
        return {'res': 'err', 'message': 'Unknown lead'}

    old_status_id = lead.status_id

    # Update lead
    lead.upd_date = datetime.utcnow()
    lead.status_id = params['statusId']
    lead.amount = params['amount'] if params.get('amount') else 0
    lead.comment = params.get('comment')
    if params.get('archived') is not None:
        lead.archived = params['archived']

    # Log action
    new_action = LeadAction()
    new_action.type = LeadActionType.update_lead
    new_action.lead_id = lead.id
    new_action.nepkit_user_id = request_data['user_id']
    db.session.add(new_action)

    if old_status_id != lead.status_id:
        # Log change_status action
        new_action = LeadAction()
        new_action.type = LeadActionType.update_lead_status
        new_action.old_status_id = old_status_id
        new_action.new_status_id = lead.status_id
        new_action.lead_id = lead.id
        new_action.nepkit_user_id = request_data['user_id']
        db.session.add(new_action)

    db.session.commit()

    # Set tags and fields
    if params.get('tags'):
        lead.set_tags(params['tags'])
    if len(fields) > 0:
        lead.set_fields(fields)

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
        .filter_by(id=params['id'],
                   nepkit_installation_id=request_data['installation_id']) \
        .first()
    lead.upd_date = datetime.utcnow()
    lead.status_id = params['statusId']

    db.session.commit()

    return {
        'res': 'ok'
    }


# Complete lead tasks
def complete_lead_tasks(params, request_data):
    vld = Validator({
        'id': {'type': 'number', 'required': True},
        'taskIds': {'type': 'list', 'required': True}
    })
    is_valid = vld.validate(params)
    if not is_valid:
        return {'res': 'err', 'message': 'Invalid params', 'errors': vld.errors}

    # Get lead by id
    lead = Lead.query \
        .filter_by(id=params['id'],
                   nepkit_installation_id=request_data['installation_id']) \
        .first()
    if not lead:
        return {'res': 'err', 'message': 'Unknown lead'}

    lead.complete_tasks(params['taskIds'],
                        user_id=request_data['user_id'])

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
        .filter_by(id=params['id'],
                   nepkit_installation_id=request_data['installation_id']) \
        .first()
    lead.archived = True

    # Log action
    new_action = LeadAction()
    new_action.type = LeadActionType.archive_lead
    new_action.lead_id = lead.id
    new_action.nepkit_user_id = request_data['user_id']
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
        .filter_by(id=params['id'],
                   nepkit_installation_id=request_data['installation_id']) \
        .first()
    lead.archived = False

    # Log action
    new_action = LeadAction()
    new_action.type = LeadActionType.restore_lead
    new_action.lead_id = lead.id
    new_action.nepkit_user_id = request_data['user_id']
    db.session.add(new_action)

    db.session.commit()

    return {
        'res': 'ok'
    }
