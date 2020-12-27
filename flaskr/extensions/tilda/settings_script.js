const { React, moment, com } = window.globalEnv
const { view, app } = window.localEnv
const { useState, useEffect, useMemo } = React

const { useForm } = com.Form
const { strs, statuses, installationExtensionSettings } = view.data

view.render = () => {
  const [reqLoading, setReqLoading] = useState(false)
  const [form] = useForm()

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
          setReqLoading(true)

          app
            .sendReq('updateExtensionSettings', {
              extensionId: installationExtensionSettings.id,
              data: values
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
            'label': strs['v_extension_mottor_information_settings_status'],
            'options': statusOptions,
            'rules': [
                {'required': true,
                 'message': strs['v_extension_mottor_information_settings_primary_rules_required']}
            ]
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
