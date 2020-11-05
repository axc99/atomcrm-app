const addLead = (app, params, event) => {
    const { columnKey, columnIndex } = event
    const page = app.getView()
    const board = page.getCom('leadsBoard')
    const boardColumns = board.getAttr('columns')

    // Set loading to add button
    boardColumns[columnIndex].addLoading = true
    board.setAttr('columns', boardColumns)

    app
        .sendReq('createLead', {
            statusId: +columnKey
        })
        .then(result => {
            if (result.res === 'ok') {
                // Update leads in column
                app
                    .sendReq('getLeadComponents', {
                        statusId: +columnKey,
                        offset: 0,
                        limit: 10,
                        search: "SEARCH",
                        filter: FILTER
                    })
                    .then(result => {
                        // Unset loading to add button
                        boardColumns[columnIndex].addLoading = false
                        board.setAttr('columns', boardColumns)

                        if (result.res == 'ok') {
                            const { leadComponents, leadTotal } = result

                            // Set total and set/append items
                            boardColumns[columnIndex].total = leadTotal
                            boardColumns[columnIndex].items = leadComponents

                            board.setAttr('columns', boardColumns)
                        }
                    })
            }
        })
}