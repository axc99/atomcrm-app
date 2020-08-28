from flaskr.models.lead import Lead
from flaskr.models.status import Status
from flaskr.models.field import Field


# Get leads
def get_leads(data, veokit_system_id):
    res_leads = []

    leads_q = Lead.query.filter_by(veokit_system_id=veokit_system_id)

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
            'add_date': lead.add_date,
            'upd_date': lead.upd_date
        })

    return {
        'leads': res_leads
    }


# Create lead
def create_lead(data, veokit_system_id):
    lead = {}

    return {
        'lead': lead
    }


# Update lead
def update_lead(data, veokit_system_id):
    lead = {}

    return {
        'lead': lead
    }


# Archive lead (delete)
def archive_lead(data, veokit_system_id):
    return ()


# Get statuses
def get_statuses(data, veokit_system_id):
    res_statuses = []

    statuses_q = Status.query.filter_by(veokit_system_id=veokit_system_id)

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
def get_fields(data, veokit_system_id):
    res_fields = []

    fields_q = Field.query.filter_by(veokit_system_id=veokit_system_id)

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
