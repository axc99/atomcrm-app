const onChangePeriod = (app, params, event) => {
    const { value } = event

    app
        .getPage()
        .to({
            periodType: 'PERIOD_TYPE',
            periodFrom: value[0],
            periodTo: value[1]
        })
}