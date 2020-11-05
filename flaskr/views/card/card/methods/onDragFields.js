const onDragFields = (app, params, event) => {
    const window = app.getView()
    const fieldsTable = window.getCom('updateCardSettingsForm_fields_table')
    const rows = fieldsTable.getAttr('rows')
    const { oldIndex, newIndex } = event

    rows.splice(newIndex, 0, rows.splice(oldIndex, 1)[0])

    fieldsTable.setAttr('rows', rows)
}