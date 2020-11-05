const onFinishForm = (app, params, event) => {
    const window = app.getView()
    const form = window.getCom('createStatusForm')
    const { values } = event

    form.setAttr('loading', true)

    app
        .sendReq('createStatus', {
            name: values.name,
            color: values.color
        })
        .then(result => {
            form.setAttr('loading', false)

            if (result.res == 'ok') {
                // Reload parent page
                app.getPage().reload()
            }
        })
}