const onClickAddField = (app, params, event) => {
    const window = app.getView()
    const fieldsTable = window.getCom('updateCardSettingsForm_fields_table')
    const rows = fieldsTable.getAttr('rows')

    rows.push({
        'name': {
            '_com': 'Field.Input',
            'maxLength': 40
        },
        'valueType': {
            '_com': 'Field.Select',
            'options': VALUE_TYPE_OPTIONS,
            'value': 'string'
        },
        boardVisibility: {
            '_com': 'Field.Select',
            'value': 'subtitle',
            'options': BOARD_VISIBILITY_OPTIONS
        },
        actions: [
            {
                '_com': 'Button',
                'icon': 'delete',
                'onClick': ['onClickDeleteField', {
                    'index': rows.length
                }]
            }
        ]
    })

    fieldsTable.setAttr('rows', rows)
}