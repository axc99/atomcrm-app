from flaskr.models.status import Status


# Create status
def create_status(params):
    status = params.status


# Update status
def update_status(params):
    status = params.status


# Update statuses
def update_statuses(params):
    for status in params.statuses:
        pass


def delete_status(params):
    if params['statusId']:
        Status.query\
            .filter_by(id=params['statusId'])\
            .delete()

    # if params.assignedStatusId:
    #     Lead.query.filter_by()
    # else:
    #     pass
