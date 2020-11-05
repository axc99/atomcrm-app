const onSearchLeads = (app, params, event) => {
    app
        .getPage()
        .to({
            search: event.value
        })
}