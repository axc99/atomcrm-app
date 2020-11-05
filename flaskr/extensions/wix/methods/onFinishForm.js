const onFinishForm = (app, args, event) => {
    const page = app.getPage()
    const form = page.getCom('extensionSettingsForm')
    const mappingTable = page.getCom('extensionSettingsForm_mapping_table')
    const rows = mappingTable.getAttr('rows')
    const { values } = event

    const data = {
        ...values,
        mapping: []
    }
    rows.map(row => {
        data.mapping.push({
            key: row.key,
            field: row.field.value
        })
    })

    form.setAttr('loading', true)
    app
        .sendReq('updateExtensionSettings', {
            extensionId: INSTALLATION_EXTENSION_SETTINGS_ID,
            data
        })
        .then(result => {
            form.setAttr('loading', false)
        })
}