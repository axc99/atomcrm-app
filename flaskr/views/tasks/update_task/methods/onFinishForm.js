const onFinishForm =(app, params, event) => {
    const window = app.getView()
    const form = window.getCom('updateTaskForm')
    const tasksSetsTable = window.getCom('updateTaskForm_tasks_table')
    const rows = tasksSetsTable.getAttr('rows')
    const { values } = event

    form.setAttr('loading', true)

    const tasks = []
    rows.map(row => {
        tasks.push({
            id: row.key,
            name: row.name.value
        })
    })

    app
        .sendReq('updateTask', {
            id: TASK_ID,
            name: values.name,
            tasks
        })
        .then(result => {
            form.setAttr('loading', false)

            if (result.res == 'ok') {
                // Reload parent page
                app.getPage().reload()
            }
        })
}