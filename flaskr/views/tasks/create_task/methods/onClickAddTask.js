const onClickAddTask = (app, params, event) => {
    const window = app.getView()
    const tasksSetsTable = window.getCom('createTaskForm_tasks_table')
    const rows = tasksSetsTable.getAttr('rows')

    rows.push({
        'name': {
            '_com': 'Field.Input'
        },
        actions: [
            {
                '_com': 'Button',
                'icon': 'delete',
                'onClick': ['onClickDeleteTask', {
                    'index': rows.length
                }]
            }
        ]
    })

    tasksSetsTable.setAttr('rows', rows)
}