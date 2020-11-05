const onDragStatus = (app, params, event) => {
    const { key, newIndex, oldIndex } = event
    const window = app.getView()
    const list = window.getCom('statusesList')
    const items = list.getAttr('items')

    items.splice(newIndex, 0, items.splice(oldIndex, 1)[0])

    list.setAttr('items', items)

    app.sendReq('updateStatusIndex', {
        id: key,
        newIndex
    })
}