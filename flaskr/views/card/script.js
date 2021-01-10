const { React, moment, com } = window.globalEnv
const { view, app } = window.localEnv
const { useState, useEffect, useMemo } = React

const { useForm } = com.Form
const { strs, statusColors } = view.data

const linesToJson = (lines) => {
  const json = {}

  lines.split('\n').map(line => {
    const [key, value] = line.split('=')
    json[key] = value
  })

  return json
}

const jsonToLines = (json) => {
  if (!json) {
    json = {}
  }

  let lines = []

  Object.entries(json).map(([key, value]) => {
    lines.push(`${key}=${value}`)
  })

  return lines.join('\n')
}

const FormFields = ({ fields, setFields, loading }) => {
  const tableRows = []
  const valueTypeOptions = [
    {
      value: 'string',
      label: strs['form_fields_table_valueType_string']
    },
    {
      value: 'email',
      label: strs['form_fields_table_valueType_email']
    },
    {
      value: 'phone',
      label: strs['form_fields_table_valueType_phone']
    },
    {
      value: 'long_string',
      label: strs['form_fields_table_valueType_longString']
    },
    {
      value: 'number',
      label: strs['form_fields_table_valueType_number']
    },
    {
      value: 'boolean',
      label: strs['form_fields_table_valueType_boolean']
    },
    {
      value: 'date',
      label: strs['form_fields_table_valueType_date']
    },
    {
      value: 'choice',
      label: strs['form_fields_table_valueType_choice']
    }
  ]
  const boardVisibilityOptions = [
    {
      value: null,
      label: strs['form_fields_table_boardVisibility_none']
    },
    {
      value: 'title',
      label: strs['form_fields_table_boardVisibility_title']
    },
    {
      value: 'subtitle',
      label: strs['form_fields_table_boardVisibility_subtitle']
    }
  ]

  const addField = () => {
    fields.push({
      name: '',
      valueType: 'string',
      boardVisibility: 'subtitle'
    })
    setFields([...fields])
  }

  const updateField = (i, subtask) => {
    fields[i] = subtask
    setFields([...fields])
  }

  const removeField = (i) => {
    fields.splice(i, 1)
    setFields([...fields])
  }

  const moveField = (oldIndex, newIndex) => {
    fields.splice(newIndex, 0, fields.splice(oldIndex, 1)[0])
    setFields([...fields])
  }

  fields.map((field, i) => {
    tableRows.push({
      key: field.id,
      name: {
        _com: 'Field.Input',
        value: field.name,
        maxLength: 40,
        onChange: ({ value }) => updateField(i, { ...field, name: value }),
      },
      valueType: [
        {
          _com: 'Field.Select',
          onChange: ({ value }) => updateField(i, { ...field, valueType: value }),
          options: valueTypeOptions,
          value: field.valueType
        },
        field.valueType == 'choice' && {
          _com: 'Field.Input',
          onChange: ({ value }) => updateField(i, { ...field, choiceOptions: value }),
          multiline: true,
          maxLength: 500,
          placeholder: 'key=value',
          value: field.choiceOptions
        }
      ],
      boardVisibility: {
        _com: 'Field.Select',
         onChange: ({ value }) => updateField(i, { ...field, boardVisibility: value }),
        options: boardVisibilityOptions,
        value: field.boardVisibility
      },
      actions: [
        {
          _com: 'Button',
          icon: 'delete',
          onClick: () => removeField(i)
        }
      ]
    })
  })

  return [
    {
      _com: 'Table',
      draggable: true,
      loading,
      emptyText: strs['form_fields_table_noFields'],
      onDrag: ({ oldIndex, newIndex }) => {
        moveField(oldIndex, newIndex)
      },
      columns: [
        {
          width: 35,
          key: 'name',
          title: strs['form_fields_table_field']
        },
        {
          width: 35,
          key: 'valueType',
          title: strs['form_fields_table_valueType']
        },
        {
          width: 30,
          key: 'boardVisibility',
          title: strs['form_fields_table_boardVisibility']
        }
      ],
      rows: tableRows
    },
    {
      _com: 'Button',
      label: strs['form_fields_addField'],
      icon: 'plus',
      type: 'solid',
      onClick: () => addField()
    }
  ]
}

view.render = () => {
  const [form] = useForm()
  const [reqLoading, setReqLoading] = useState(false)
  const [data, setData] = useState({
    installationCardSettings: view.data.installationCardSettings,
    currencies: view.data.currencies,
    fields: [],
    loading: false
  })
  const setFields = fields => {
    setData({
      ...data,
      fields
    })
  }
  const [currencyEnabled, setCurrencyEnabled] = useState(data.installationCardSettings.amountEnabled)

  useEffect(() => {
    loadFields()
  }, [])

  useEffect(() => {
    form.setFieldsValue({
      amountEnabled: data.installationCardSettings.amountEnabled,
      currency: data.installationCardSettings.currency
    })
  }, [data])

  const loadFields = () => {
    setData({
      ...data,
      fields: [],
      loading: true
    })

    app
      .sendReq('getFields', {})
      .then(result => {
        const { res, fields } = result

        if (res == 'ok') {
          setData({
            ...data,
            fields: fields.map(field => {
              return {
                ...field,
                choiceOptions: jsonToLines(field.choiceOptions)
              }
            }),
            loading: false
          })
        }
      })
  }

  const currencyOptions = data.currencies.map(currency => ({
    'value': currency['key'],
    'label': `${currency['code']} - ${currency['namePlural']}`
  }))

  return {
    header: {
      title: strs['name']
    },
    scheme: [
      {
        _com: 'Form',
        form,
        onValuesChange: ({ values }) => {
          if (values.amountEnabled !== undefined) {
            setCurrencyEnabled(values.amountEnabled)
          }
        },
        onFinish: ({ values }) => {
          setReqLoading(true)
          app
            .sendReq('updateCardSettings', {
                amountEnabled: values.amountEnabled,
                currency: values.currency,
                fields: data.fields.map(field => {
                  return {
                    ...field,
                    choiceOptions: linesToJson(field.choiceOptions)
                  }
                })
            })
            .then(result => {
                setReqLoading(false)

                if (result.res == 'ok') {
                    app.showNotification({
                        message: strs['notification_changesSaved'],
                        duration: 1
                    })
                }
            })
        },
        fields: [
          {
            _com: 'Field.Checkbox',
            key: 'amountEnabled',
            text: strs['form_leadAmount']
          },
          {
            _com: 'Field.Select',
            key: 'currency',
            withSearch: true,
            disabled: !currencyEnabled,
            label: strs['form_amountCurrency'],
            options: currencyOptions,
            shouldUpdate: true
          },
          {
            _com: 'Field.Custom',
            columnWidth: 12,
            label: strs['form_fields'],
            content:
              FormFields({
                loading: data.loading,
                fields: data.fields,
                setFields
              })
          }
        ],
        buttons: [
          {
            _com: 'Button',
            type: 'primary',
            submitForm: true,
            loading: reqLoading,
            icon: 'save',
            label: strs['form_save']
          }
        ]
      }
    ]
  }
}
