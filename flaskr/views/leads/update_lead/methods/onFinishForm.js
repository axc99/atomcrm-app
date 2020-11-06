const onFinishForm = (app, params, event) => {
    const { values } = event

    const window = app.getView()
    const form = window.getCom('updateLeadForm')
    const originalStatusId = ORIGINAL_STATUS_ID
    const amount = +window.getCom('updateLeadForm_amount').getAttr('value')
    const statusId = window.getCom('updateLeadForm_status').getAttr('value')
    const tags = window.getCom('updateLeadForm_tags').getAttr('value')

    const fields = []
    Object.entries(values).map(([key, value]) => {
        fields.push({
            fieldId: +key,
            value: value
        })
    })

    form.setAttr('loading', true)

    app
        .sendReq('updateLead', {
            id: LEAD_ID,
            amount,
            fields,
            tags,
            statusId
        })
        .then(result => {
            form.setAttr('loading', false)

            if (result.res == 'ok') {
                if (statusId != originalStatusId) {
                    // Update status columns
                    app.getPage().callMethod('loadLeads', { statusId: originalStatusId })
                    app.getPage().callMethod('loadLeads', { statusId })
                } else {
                    // Update status column
                    app.getPage().callMethod('loadLeads', { statusId: originalStatusId })
                }

                app.showNotification({
                    message: 'SAVING_NOTIFICATION_MESSAGE',
                    duration: 1
                })
            }
        })
}