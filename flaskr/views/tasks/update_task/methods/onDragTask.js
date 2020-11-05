const onDragTask = (app, params, event) => {
    const window = app.getView()
    const tasksTable = window.getCom('updateTaskForm_tasks_table')
    const rows = tasksTable.getAttr('rows')
    const { oldIndex, newIndex } = event

    rows.splice(newIndex, 0, rows.splice(oldIndex, 1)[0])

    tasksTable.setAttr('rows', rows)
}