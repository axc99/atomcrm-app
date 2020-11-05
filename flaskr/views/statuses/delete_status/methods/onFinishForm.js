const onFinishForm = (app, params, event) => {
    const window = app.getView()
    const form = window.getCom('deleteStatusForm')
    const { values } = event

    const assignedStatusId = values.action == 'deleteLeads' ? null : +values.action

    form.setAttr('loading', true)
    app
        .sendReq('deleteStatus', {
            id: STATUS_ID,
            assignedStatusId
        })
        .then(result => {
            form.setAttr('loading', false)

            if (result.res == 'ok') {
                // Reload parent page
                app.getPage().reload()
            }
        })
}