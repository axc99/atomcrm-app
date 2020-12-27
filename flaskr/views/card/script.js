const { React, moment, com } = window.globalEnv
const { view, app } = window.localEnv
const { useState, useEffect, useMemo } = React

const { useForm } = com.Form
const { strs, statusColors } = view.data

const FormFields = ({ fields, setFields }) => {
  const tableRows = []
  const valueTypeOptions = [
    {
      value: 'string',
      label: strs['schema_form_fields_table_string']
    },
    {
      value: 'email',
      label: strs['schema_form_fields_table_email']
    },
    {
      value: 'phone',
      label: strs['schema_form_fields_table_phone']
    },
    {
      value: 'long_string',
      label: strs['schema_form_fields_table_longString']
    },
    {
      value: 'number',
      label: strs['schema_form_fields_table_number']
    },
    {
      value: 'boolean',
      label: strs['schema_form_fields_table_boolean']
    },
    {
      value: 'date',
      label: strs['schema_form_fields_table_date']
    },
    {
      value: 'choice',
      label: strs['schema_form_fields_table_choice']
    }
  ]
  const boardVisibilityOptions = [
    {
      value: null,
      label: strs['schema_form_fields_table_none']
    },
    {
      value: 'title',
      label: strs['schema_form_fields_table_title']
    },
    {
      value: 'subtitle',
      label: strs['schema_form_fields_table_subtitle']
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
      emptyText: strs['scheme_form_fields_table_noFields'],
      onDrag: ({ oldIndex, newIndex }) => {
        moveField(oldIndex, newIndex)
      },
      columns: [
        {
          width: 35,
          key: 'name',
          title: strs['scheme_form_fields_table_field']
        },
        {
          width: 35,
          key: 'valueType',
          title: strs['scheme_form_fields_table_valueType']
        },
        {
          width: 30,
          key: 'boardVisibility',
          title: strs['scheme_form_fields_table_boardVisibility']
        }
      ],
      rows: tableRows
    },
    {
      _com: 'Button',
      label: strs['scheme_form_fields_addField'],
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
            fields,
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
    schema: [
      {
        _com: 'Form',
        form,
        onFinish: ({ values }) => {
          setReqLoading(true)
          app
            .sendReq('updateCardSettings', {
                amountEnabled: values.amountEnabled,
                currency: values.currency,
                fields: data.fields
            })
            .then(result => {
                setReqLoading(false)

                if (result.res == 'ok') {
                    app.showNotification({
                        message: strs['changesSaved'],
                        duration: 1
                    })
                }
            })
        },
        fields: [
          {
            _com: 'Field.Checkbox',
            key: 'amountEnabled',
            text: strs['scheme_form_leadAmount'],
            onChange: 'onChangeAmountEnabled'
          },
          {
            _com: 'Field.Select',
            key: 'currency',
            withSearch: true,
            disabled: !data.installationCardSettings.amountEnabled,
            label: strs['scheme_form_amountCurrency'],
            options: currencyOptions
          },
          {
            _com: 'Field.Custom',
            columnWidth: 12,
            label: strs['scheme_form_fields'],
            content:
              FormFields({
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
            label: strs['scheme_form_save']
          }
        ]
      }
    ]
  }
}
