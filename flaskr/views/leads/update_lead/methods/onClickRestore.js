const onClickRestore = (app, params, event) => {
    const window = app.getWindow()

    app
        .sendReq('restoreLead', {
            id: LEAD_ID
        })
        .then(result => {
            if (result.res == 'ok') {
                // Reload parent window
                app.getWindow().reload()

                // Reload leads on page
                app.getPage().callMethod('loadLeads', { statusId: STATUS_ID })

                window.close()
            }
        })
}