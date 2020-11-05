const deleteStatus = (app, params) => {
    const { id } = params
    const window = app.getView()
    const list = window.getCom('statusesList')

    const items = list.getAttr('items')
    const item = items.find(item => item.key == id)

    // Set loading to delete button
    item.actions[1].loading = true
    list.setAttr('items', items)

    app
        .sendReq('deleteStatus', {
            id
        })
        .then(result => {
            // Unset loading to delete button
            item.actions[1].loading = false
            list.setAttr('items', items)

            if (result.res == 'ok') {
                // Reload parent page
                app.getPage().reload()
            }
        })
}