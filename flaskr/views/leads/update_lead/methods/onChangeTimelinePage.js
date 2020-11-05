const onChangeTimelinePage = (app, params, event) => {
    app.getWindow().to({
        id: LEAD_ID,
        tab: 'activity',
        page: event.page
    })
}