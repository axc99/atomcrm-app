const { React, moment, com } = window.globalEnv
const { view, app } = window.localEnv
const { useState, useEffect, useMemo } = React

const { useForm } = com.Form
const { strs, statusColors } = view.data

const linesToJson = (lines) => {
  const json = {}

  if (lines) {
    lines
      .split('\n')
      .map(line => {
        const [key, value] = line.split('=')
        json[key] = value
      })
  }

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
      value: 'none',
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
  const [activeTab, setActiveTab] = useState('general')
  const [data, setData] = useState({
    installationSettings: view.data.installationSettings,
    currencies: view.data.currencies,
    fields: [],
    loading: false
  })

  useEffect(() => {
    loadFields()
  }, [])

  const loadFields = () => {
    setData(data => ({
      ...data,
      fields: [],
      loading: true
    }))

    app
      .sendReq('getFields', {})
      .then(result => {
        const { res, fields } = result

        if (res == 'ok') {
          setData(data => ({
            ...data,
            fields: fields.map(field => {
              return {
                ...field,
                choiceOptions: jsonToLines(field.choiceOptions)
              }
            }),
            loading: false
          }))
        }
      })
  }

  return {
    header: {
      title: strs['name'],
      onChangeTab: ({ key }) => setActiveTab(key),
      tabs: [
        {
          'key': 'general',
          'text': strs['header_general'],
          'active': activeTab === 'general'
        },
        {
          'key': 'tasks',
          'text': strs['header_tasks'],
          'active': activeTab === 'tasks'
        }
      ]
    },
    scheme: [
      {
        general: CardGeneral({
          data,
          setData
        }),
        tasks: CardTasks({
          data,
          setData
        }),
      }[activeTab]
    ]
  }
}

const CardGeneral = ({ data, setData }) => {
  const [form] = useForm()
  const [reqLoading, setReqLoading] = useState(false)

  useEffect(() => {
    form.setFieldsValue({
      amountEnabled: data.installationSettings.amountEnabled,
      currency: data.installationSettings.currency
    })
  }, [data])

  const setFields = fields => {
    setData({
      ...data,
      fields
    })
  }

  const currencyOptions = data.currencies.map(currency => ({
    'value': currency['key'],
    'label': `${currency['code']} - ${currency['namePlural']}`
  }))

  console.debug('data', data)

  return {
    _com: 'Form',
    form,
    onValuesChange: ({ values }) => {
      console.debug('values', values)
      setData({
        ...data,
        installationSettings: {
          ...data.installationSettings,
          amountEnabled: values.amountEnabled === undefined ? data.installationSettings.amountEnabled : values.amountEnabled,
          currency: values.currency === undefined ? data.installationSettings.currency : values.currency
        }
      })
    },
    onFinish: ({ values }) => {
      setReqLoading(true)
      app
        .sendReq('updateSettings', {
            amountEnabled: values.amountEnabled,
            currency: values.currency,
            fields: data.fields.map(field => {
              return {
                ...field,
                choiceOptions: field.choiceOptions && linesToJson(field.choiceOptions)
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
        disabled: !data.installationSettings.amountEnabled,
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
}

const CardTasksList = ({ tasks, deleteLoadingIndex, loading, openModal, deleteTask, onDragTask }) => {
  const items = tasks.map((task, i) => {
    const deleteButton = {
      _com: 'Button',
      icon: 'delete',
      loading:  deleteLoadingIndex !== null && (i === deleteLoadingIndex),
      onClick: () => deleteTask({
        id: task.id,
        completedCount: task.completedCount
      })
    }

    return {
      key: task.id,
      color: task.color,
      title: task.name,
      actions: [
        {
          _com: 'Button',
          icon: 'edit',
          label: strs['tasks_table_editTask'],
          onClick: () => openModal({
            type: 'update',
            task
          })
        },
        deleteButton
      ]
    }
  })

  return {
    _com: 'List',
    _id: 'tasksList',
    draggable: true,
    loading,
    emptyText: strs['tasks_table_noTasks'],
    onDrag: onDragTask,
    items
  }
}

const CardTasksModal = ({ opened=false, type, closeModal, task, loadTasks }) => {
  const [form] = useForm()
  const [reqLoading, setReqLoading] = useState(false)

  useEffect(() => {
    if (opened) {
      if (task) {
        form.setFieldsValue({
          name: task.name
        })
      } else {
        form.setFieldsValue({
          name: ''
        })
      }
    }
  }, [task, opened])

  return {
    _com: 'Modal',
    opened,
    onCancel: () => closeModal(),
    title: type === 'create' ? strs['tasks_taskModal_createTitle'] : strs['tasks_taskModal_updateTitle'],
    content: [
      {
        _com: 'Form',
        form,
        onFinish: ({ values }) => {
          setReqLoading(true)
          app
            .sendReq(type === 'create' ? 'createTask' : 'updateTask', {
              id: task && task.id,
              name: values.name
            })
            .then(result => {
              setReqLoading(false)

              if (result.res == 'ok') {
                closeModal()
                loadTasks()
              }
            })
        },
        fields: [
          {
            _com: 'Field.Input',
            type: 'text',
            key: 'name',
            label: strs['tasks_taskModal_form_name'],
            placeholder: strs['tasks_taskModal_form_name_placeholder'],
            maxLength: 30,
            rules: [
              {max: 30, message: strs['tasks_taskModal_form_name_length']},
              {required: true, message: strs['tasks_taskModal_form_name_required']}
            ]
          }
        ],
        buttons: [
          {
            _com: 'Button',
            type: 'primary',
            submitForm: true,
            loading: reqLoading,
            icon: type === 'create' ? 'plus' : 'save',
            label: type === 'create' ? strs['tasks_taskModal_form_create'] : strs['tasks_taskModal_form_save']
          }
        ]
    }
    ]
  }
}

const CardTasksDeleteModal = ({ id, opened, closeDeleteModal, loadTasks, tasks }) => {
  const [reqLoading, setReqLoading] = useState(false)

  return {
    _com: 'Modal',
    title: strs['tasks_deleteTaskModal_title'],
    subtitle: strs['tasks_deleteTaskModal_subtitle'],
    buttons: [
       {
          _com: 'Button',
          type: 'danger',
          icon: 'delete',
          label: strs['tasks_deleteTaskModal_delete'],
          onClick: () => {
            setReqLoading(false)
            app
              .sendReq('deleteTask', { id })
              .then(result => {
                setReqLoading(false)

                if (result.res == 'ok') {
                  closeDeleteModal()
                  loadTasks()
                }
              })
          }
        }
    ],
    opened,
    onCancel: () => closeDeleteModal()
  }
}

const CardTasks = () => {
  const [listData, setListData] = useState({
    tasks: [],
    loading: true
  })
  const [taskModal, setTaskModal] = useState({
    task: null,
    type: 'create', // create | update
    opened: false
  })
  const [deleteTaskModal, setDeleteTaskModal] = useState({
    id: null,
    opened: false
  })

  const loadTasks = () => {
    setListData({
      tasks: [],
      loading: true
    })

    app
      .sendReq('getTasks', {})
      .then(result => {
        const { res, tasks } = result

        if (res == 'ok') {
          setListData({
            tasks,
            loading: false
          })
        }
      })
  }

  useEffect(() => {
    loadTasks()
  }, [])

  // Open create/update modal
  const openModal = ({ type, task }) => {
    setTaskModal({
      task,
      type,
      opened: true
    })
  }

  // Close create/update modal
  const closeModal = () => {
    setTaskModal({
      ...taskModal,
      opened: false
    })
  }

  // Open delete modal
  const openDeleteModal = ({ id }) => {
    setDeleteTaskModal({
      id,
      opened: true
    })
  }

  // Close delete modal
  const closeDeleteModal = () => {
    setDeleteTaskModal({
      ...deleteTaskModal,
      opened: false
    })
  }

  // Handle drag task
  const onDragTask = ({ key, oldIndex, newIndex }) => {
    listData.tasks.splice(newIndex, 0, listData.tasks.splice(oldIndex, 1)[0])
    setListData({ ...listData })

    app
      .sendReq('updateTaskIndex', {
        id: key,
        newIndex
      })
  }

  // Handle delete task
  const deleteTask = ({ id, completedCount }) => {
    if (completedCount > 0) {
      openDeleteModal({ id })
    } else {
      const deletedItemIndex = listData.tasks.findIndex(task => task.id == id)
      setListData({
        ...listData,
        deleteLoadingIndex: deletedItemIndex
      })

      app
        .sendReq('deleteTask', { id })
        .then(result => {
          if (result.res == 'ok') {
            listData.tasks.splice(deletedItemIndex, 1)
            setListData({
              ...listData,
              deleteLoadingIndex: null,
              tasks: listData.tasks
            })
          }
        })
    }
  }

  return [
    CardTasksList({
      ...listData,
      openModal,
      onDragTask,
      deleteTask
    }),
    {
      _com: 'Button',
      label: strs['tasks_createTask'],
      icon: 'plus',
      type: 'primary',
      onClick: () => openModal({ type: 'create' })
    },
    CardTasksModal({
      ...taskModal,
      loadTasks,
      closeModal
    }),
    CardTasksDeleteModal({
      ...deleteTaskModal,
      closeDeleteModal,
      loadTasks,
      tasks: listData.tasks
    })
  ]
}

