const onFinishForm = (app, params, event) => {
    const { values } = event

    app
        .getPage()
        .to({
            periodFrom: values.period ? values.period[0] : undefined,
            periodTo: values.period ? values.period[1] : undefined,
            archived: values.archived ? values.archived : undefined,
            utmSource: values.utmSource,
            utmMedium: values.utmMedium,
            utmCampaign: values.utmCampaign,
            utmTerm: values.utmTerm,
            utmContent: values.utmContent
        })
}