const onChangeValueType = (app, params, event) => {
    const { fieldIndex } = params
    const { value } = event
    const window = app.getView()
    const fieldsTable = window.getCom('updateCardSettingsForm_fields_table')
    const rows = fieldsTable.getAttr('rows')

    if (value === 'choice') {
        rows[fieldIndex]['valueType'][1] = {
            '_com': 'Field.Input',
            'multiline': true,
            'maxLength': 500,
            'placeholder': 'key=value'
        }
    } else {
        delete rows[fieldIndex]['valueType'][1]
    }

    fieldsTable.setAttr('rows', rows)
}
