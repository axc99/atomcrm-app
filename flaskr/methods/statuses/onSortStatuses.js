(app, params) => {
    const { key, oldIndex, newIndex } = params.row

    app.sendRequest('updateStatuses', {
        statuses: [
            {
                key: '111'
            },
            {
                key: '222'
            }
        ]
    })
}
