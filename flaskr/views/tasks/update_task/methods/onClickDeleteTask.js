const onClickDeleteTask = (app, params, event) => {
    const window = app.getView()
    const tasksTable = window.getCom('updateTaskForm_tasks_table')
    let rows = tasksTable.getAttr('rows')
    delete rows[params.index]
    tasksTable.setAttr('rows', rows)
}