const onClickDeleteField = (app, params, event) => {
    const window = app.getView()
    const fieldsTable = window.getCom('updateCardSettingsForm_fields_table')
    let rows = fieldsTable.getAttr('rows')
    delete rows[params.index]
    fieldsTable.setAttr('rows', rows)
}