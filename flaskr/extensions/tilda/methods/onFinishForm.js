const onFinishForm = (app, args, event) => {
    const window = app.getView()
    const form = window.getCom('extensionSettingsForm')
    const { values } = event

    form.setAttr('loading', true)

    app
        .sendReq('updateExtensionSettings', {
            extensionId: INSTALLATION_EXTENSION_SETTINGS_ID,
            data: values
        })
        .then(result => {
            form.setAttr('loading', false)
        })
}