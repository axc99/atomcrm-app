const onFinishForm = (app, params, e) => {
    const view = app.getView()
    const getTokenBtn = view.getCom('getTokenBtn')
    const tokenInput = view.getCom('tokenInput')

    getTokenBtn.setAttr('loading', true)

    // Get new token
    app
        .sendReq('getToken', {})
        .then(result => {
            if (result.res == 'ok') {
                tokenInput.setAttrs({
                    _vis: true,
                    value: result.token
                })

                getTokenBtn.setAttrs({
                    _vis: false,
                    loading: false
                })
            }
        })
}