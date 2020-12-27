const { React, moment, com } = window.globalEnv
const { view, app } = window.localEnv
const { useState, useEffect, useMemo } = React

const { useForm } = com.Form
const { strs, statuses, fields, wixFields, installationExtensionSettings } = view.data

const MappingFields = ({ mappingFields, setMappingFields }) => {
  const fieldOptions = [
    {'value': 0, 'label': 'Не указано'}
  ]
  fields.map(field => {
    fieldOptions.push({
      'value': field['id'],
      'label': field['name']
    })
  })

  const tableRows = []
  wixFields.map(wixField => {
    console.log('mappingFields', mappingFields)
    const mappingField = mappingFields.find(field => field['key'] === wixField['key'])
    const mappingValue = mappingField && mappingField['field']

    tableRows.push({
     'key': wixField['key'],
     'wixField': wixField['name'],
     'field': {
       '_com': 'Field.Select',
       'value': mappingValue || 0,
       'options': fieldOptions,
       'onChange': ({ value }) => {
          if (mappingField) {
            mappingField['field'] = value
          } else {
            mappingFields.push({
              key: wixField['key'],
              field: value
            })
          }

          setMappingFields([ ...mappingFields ])
       }
     }
    })
  })

  return {
    '_com': 'Table',
    '_id': 'extensionSettingsForm_mapping_table',
    'columns': [
      {
        'width': 50,
        'key': 'wixField',
        'title': 'Поле в Wix'
      },
      {
        'width': 50,
        'key': 'field',
        'title': 'Поле в AtomCRM'
      }
    ],
    'rows': tableRows
  }
}

view.render = () => {
  const [reqLoading, setReqLoading] = useState(false)
  const [form] = useForm()
  const [mappingFields, setMappingFields] = useState(installationExtensionSettings.data['mapping'])

  const statusOptions = [
    {
      'value': 'first',
      'label': strs['v_extension_wix_information_settings_status_alwaysFirst']
    }
  ]
  statuses.map(status => {
    statusOptions.push({
      value: status.id,
      color: status.color,
      label: status.name
    })
  })

  useEffect(() => {
    form.setFieldsValue({
      defaultStatus: installationExtensionSettings.data['defaultStatus']
    })
  }, [installationExtensionSettings])

  return {
    header: view.header,
    schema: [
      {
        _com: 'Form',
        form,
        onFinish: ({ values }) => {
          const data = {
            ...values,
            mapping: mappingFields
          }

          setReqLoading(true)
          app
              .sendReq('updateExtensionSettings', {
                  extensionId: installationExtensionSettings['id'],
                  data
              })
              .then(result => {
                  setReqLoading(false)

                  app.showNotification({
                    message: 'SAVING_NOTIFICATION_MESSAGE',
                    duration: 1
                  })
              })
        },
        'fields': [
          {
            '_com': 'Field.Select',
            'key': 'defaultStatus',
            'label': strs['v_extension_wix_information_settings_status'],
            'options': statusOptions,
            'rules': [
              {'required': true,
               'message': strs['v_extension_wix_information_settings_primary_rules_required']}
            ]
          },
          {
            '_com': 'Field.Custom',
            'columnWidth': 8,
            'label': 'Соотношение полей',
            'content': (
              MappingFields({
                mappingFields,
                setMappingFields
              })
            )
          }
        ],
        'buttons': [
          {
            '_com': 'Button',
            'type': 'primary',
            'submitForm': true,
            'loading': reqLoading,
            'icon': 'save',
            'label': strs['v_extension_wix_information_settings_save']
          }
        ]
    }
    ]
  }
}
