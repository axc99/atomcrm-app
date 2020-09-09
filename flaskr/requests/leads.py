from flaskr import db
from flaskr.models.lead import Lead


# Create lead
def create_lead(params, request_data):
    new_lead = Lead()
    new_lead.status_id = params['statusId']
    new_lead.veokit_installation_id = request_data['installation_id']

    db.session.add(new_lead)
    db.session.commit()

    return {
        'lead_id': new_lead.id
    }