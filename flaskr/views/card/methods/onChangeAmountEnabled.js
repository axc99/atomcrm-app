const onChangeAmountEnabled = (app, params, event) => {
    const { value } = event
    const page = app.getPage()
    const form = page.getCom('updateCardSettingsForm')
    const fields = form.getAttr('fields')

    const currencyField = fields.find(f => f.key == 'currency')
    currencyField.disabled = !value

    form.setAttr('fields', fields)
}