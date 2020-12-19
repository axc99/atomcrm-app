const onFinishForm = (app, params, event) => {
    const { values } = event
    const page = app.getPage()
    const form = page.getCom('updateCardSettingsForm')
    const fieldsTable = page.getCom('updateCardSettingsForm_fields_table')
    const rows = fieldsTable.getAttr('rows')

    form.setAttr('loading', true)

    const fields = []
    rows.map(row => {
        fields.push({
            id: row.key,
            name: row.name.value,
            valueType: row.valueType[0].value,
            choiceOptions: row.valueType[1] && row.valueType[1].value,
            boardVisibility: row.boardVisibility.value
        })
    })

    app
        .sendReq('updateCardSettings', {
            amountEnabled: values.amountEnabled,
            currency: values.currency,
            fields
        })
        .then(result => {
            form.setAttr('loading', false)

            if (result.res == 'ok') {
                app.showNotification({
                    message: 'SAVING_NOTIFICATION_MESSAGE',
                    duration: 1
                })
            }
        })
}