const loadLeads = (app, params) => {
    const { statusId, addToEnd=false } = params
    const page = app.getView()
    const board = page.getCom('leadsBoard')
    const boardColumns = board.getAttr('columns')
    const columnIndex = boardColumns.findIndex(c => c.key == statusId)

    // Set loading to load button
    boardColumns[columnIndex].loading = true
    board.setAttr('columns', boardColumns)

    app
        .sendReq('getLeadComponents', {
            statusId,
            offset: addToEnd ? boardColumns[columnIndex].items.length : 0,
            limit: (addToEnd || boardColumns[columnIndex].items.length < 10) ? 10 : boardColumns[columnIndex].items.length,
            search: "SEARCH",
            filter: FILTER
        })
        .then(result => {
            // Unset loading to load button
            boardColumns[columnIndex].loading = false
            board.setAttr('columns', boardColumns)

            if (result.res === 'ok') {
                const { leadComponents, leadTotal, leadAmountSumStr } = result

                // Set total and set/append items
                boardColumns[columnIndex].total = leadTotal
                if (leadAmountSumStr) {
                    boardColumns[columnIndex].subtitle = leadAmountSumStr
                }
                boardColumns[columnIndex].items = !addToEnd ? leadComponents : [
                    ...boardColumns[columnIndex].items,
                    ...leadComponents
                ]

                board.setAttr('columns', boardColumns)
            }
        })
}