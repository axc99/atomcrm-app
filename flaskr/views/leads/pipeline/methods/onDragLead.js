const onDragLead = (app, params, event) => {
    const { key, oldColumnIndex, newColumnIndex, newColumnKey, oldItemIndex, newItemIndex } = event
    const page = app.getView()
    const board = page.getCom('leadsBoard')
    const boardColumns = board.getAttr('columns')

    // Get item from old column
    const item = boardColumns[oldColumnIndex].items[oldItemIndex]
    // Remove item from column
    boardColumns[oldColumnIndex].items.splice(oldItemIndex, 1)
    // Add item new column
    boardColumns[newColumnIndex].items.splice(newItemIndex, 0, item)
    // Sort by order attr
    boardColumns[newColumnIndex].items.sort((a, b) => a.order < b.order)

    // Update columns on board
    board.setAttr('columns', boardColumns)

    app
        .sendReq('updateLeadStatus', {
            id: key,
            statusId: +newColumnKey
        })
        .then(result => {
            // Unset loading to both columns
            app.getPage().callMethod('loadLeads', { statusId: boardColumns[oldColumnIndex].key })
            app.getPage().callMethod('loadLeads', { statusId: boardColumns[newColumnIndex].key })
        })
}