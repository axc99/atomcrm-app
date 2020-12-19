const onChangePeriodType = (app, params, event) => {
    const { value } = event

    app
        .getPage()
        .to({
            periodType: value
        })
}