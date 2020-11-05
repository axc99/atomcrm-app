const onChangeTasks = (app, params, event) => {
    const { value } = event
    const task_ids = value

    app
        .sendReq('completeLeadTasks', {
            id: LEAD_ID,
            task_ids
        })
        .then(result => {
            if (result.res == 'ok') {
                // ...
            }
        })
}