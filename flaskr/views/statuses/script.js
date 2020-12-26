const { React, moment, com } = window.globalEnv
const { view, app } = window.localEnv
const { useState, useEffect, useMemo } = React

const { useForm } = com.Form
const { strs, statusColors } = view.data

const StatusesList = ({ statuses, deleteLoadingIndex, loading, openModal, deleteStatus, onDragStatus }) => {
  const items = statuses.map((status, i) => {
    const deleteButton = {
      _com: 'Button',
      icon: 'delete',
      loading:  deleteLoadingIndex !== null && (i === deleteLoadingIndex),
      onClick: () => deleteStatus({
        id: status.id,
        leadCount: status.leadCount
      })
    }

    return {
      key: status.id,
      color: status.color,
      title: status.name,
      extra: `${status.leadCount} ${status.leadCount == 1 ? strs['schema_count_lead'] : strs['schema_count_leads']}`,
      actions: [
        {
          _com: 'Button',
          icon: 'edit',
          label: strs['schema_editStatus'],
          onClick: () => openModal({
            type: 'update',
            status
          })
        },
        deleteButton
      ]
    }
  })

  return {
    _com: 'List',
    _id: 'statusesList',
    draggable: true,
    loading,
    emptyText: strs['schema_noStatuses'],
    onDrag: onDragStatus,
    items
  }
}

const StatusModal = ({ opened=false, type, closeModal, status, loadStatuses }) => {
  const [form] = useForm()
  const [reqLoading, setReqLoading] = useState(false)

  const colorOptions = []
  statusColors.map(c => {
    colorOptions.push({
      'value': c.key,
      'label': c.name,
      'color': c.hex
    })
  })

  useEffect(() => {
    if (opened) {
      if (status) {
        form.setFieldsValue({
          name: status.name,
          color: status.color
        })
      } else {
        form.setFieldsValue({
          name: '',
          color: 'red'
        })
      }
    }
  }, [status, opened])

  return {
    _com: 'Modal',
    opened,
    onCancel: () => closeModal(),
    title: type === 'create' ? strs['schema_statusModal_createTitle'] : strs['schema_statusModal_updateTitle'],
    content: [
      {
        _com: 'Form',
        form,
        onFinish: ({ values }) => {
          setReqLoading(true)
          app
            .sendReq(type === 'create' ? 'createStatus' : 'updateStatus', {
              id: status && status.id,
              name: values.name,
              color: values.color
            })
            .then(result => {
              setReqLoading(false)

              if (result.res == 'ok') {
                closeModal()
                loadStatuses()
              }
            })
        },
        fields: [
          {
            _com: 'Field.Input',
            type: 'text',
            key: 'name',
            label: strs['schema_statusModal_form_name'],
            placeholder: strs['schema_statusModal_form_name_placeholder'],
            maxLength: 30,
            rules: [
              {max: 30, message: strs['schema_statusModal_name_length']},
              {required: true, message: strs['schema_statusModal_name_required']}
            ]
          },
          {
            _com: 'Field.Select',
            key: 'color',
            label: strs['schema_statusModal_form_color'],
            options: colorOptions,
            rules: [
              {required: true, message: strs['schema_statusModal_form_color_required']}
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
            label: type === 'create' ? strs['schema_statusModal_form_createBtn'] : strs['schema_statusModal_form_saveBtn']
          }
        ]
    }
    ]
  }
}

const DeleteStatusModal = ({ id, opened, closeDeleteModal, loadStatuses, statuses }) => {
  const [form] = useForm()
  const [reqLoading, setReqLoading] = useState(false)

  useEffect(() => {
    if (opened) {
      form.setFieldsValue({
        action: 'deleteLeads'
      })
    }
  }, [opened])

  const selectOptions = [
    {
      'key': 'deleteLeads',
      'label': strs['schema_deleteStatusModal_form_deleteLeads']
    }
  ]

  statuses.map(status => {
    if (status.id == id) {
      return;
    }

    const hexColor = statusColors.find(c => c.key === status.color).hex

    selectOptions.push({
      'key': status.id,
      'color': hexColor,
      'label': strs['schema_deleteStatusModal_form_moveLeads']
    })
  })

  return {
    _com: 'Modal',
    title: strs['schema_deleteStatusModal_title'],
    subtitle: strs['schema_deleteStatusModal_subtitle'],
    opened,
    onCancel: () => closeDeleteModal(),
    content: [
      {
        _com: 'Form',
        form,
        onFinish: ({ values }) => {
          const { action } = values
          const assignedStatusId = action == 'deleteLeads' ? null : +action

          setReqLoading(true)
          app
            .sendReq('deleteStatus', {
              id,
              assignedStatusId
            })
            .then(result => {
              setReqLoading(false)


              if (result.res == 'ok') {
                closeDeleteModal()
                loadStatuses()
              }
            })
        },
        fields: [
          {
            _com: 'Field.Select',
            key: 'action',
            value: statuses.length > 0 ? statuses[0].id : 'deleteLeads',
            options: selectOptions
          }
        ],
        buttons: [
          {
            _com: 'Button',
            type: 'danger',
            submitForm: true,
            loading: reqLoading,
            label: strs['schema_deleteStatusModal_form_btn']
          }
        ]
    }
    ]
  }
}

view.render = () => {
  const [listData, setListData] = useState({
    statuses: [],
    loading: true,
    deleteLoadingIndex: null
  })
  const [statusModal, setStatusModal] = useState({
    status: null,
    type: 'create', // create | update
    opened: false
  })
  const [deleteStatusModal, setDeleteStatusModal] = useState({
    id: null,
    opened: false
  })

  // Open create/update modal
  const openModal = ({ type, status }) => {
    setStatusModal({
      status,
      type,
      opened: true
    })
  }

  // Close create/update modal
  const closeModal = () => {
    setStatusModal({
      ...statusModal,
      opened: false
    })
  }

  // Open delete modal
  const openDeleteModal = ({ id }) => {
    setDeleteStatusModal({
      id,
      opened: true
    })
  }

  // Close delete modal
  const closeDeleteModal = () => {
    setDeleteStatusModal({
      ...deleteStatusModal,
      opened: false
    })
  }

  const loadStatuses = () => {
    setListData({
      statuses: [],
      loading: true
    })

    app
      .sendReq('getStatuses', {})
      .then(result => {
        const { res, statuses } = result

        if (res == 'ok') {
          setListData({
            statuses,
            loading: false
          })
        }
      })
  }

  useEffect(() => {
    loadStatuses()
  }, [])

  // Handle drag status
  const onDragStatus = ({ key, oldIndex, newIndex }) => {
    listData.statuses.splice(newIndex, 0, listData.statuses.splice(oldIndex, 1)[0])
    setListData({ ...listData })

    app
      .sendReq('updateStatusIndex', {
        id: key,
        newIndex
      })
  }

  // Handle delete status
  const deleteStatus = ({ id, leadCount }) => {
    if (leadCount > 0) {
      openDeleteModal({ id })
    } else {
      const deletedItemIndex = listData.statuses.findIndex(status => status.id == id)
      setListData({
        ...listData,
        deleteLoadingIndex: deletedItemIndex
      })

      app
        .sendReq('deleteStatus', { id })
        .then(result => {
          if (result.res == 'ok') {
            listData.statuses.splice(deletedItemIndex, 1)
            setListData({
              ...listData,
              deleteLoadingIndex: null,
              statuses: listData.statuses
            })
          }
        })
    }
  }

  return {
    header: {
      title: strs['name'],
      actions: [
        {
          _com: 'Button',
          label: strs['header_createStatus'],
          type: 'primary',
          icon: 'plus',
          onClick: () => openModal({ type: 'create' })
        }
      ]
    },
    schema: [
      StatusesList({
        ...listData,
        openModal,
        onDragStatus,
        deleteStatus
      }),
      StatusModal({
        ...statusModal,
        loadStatuses,
        closeModal
      }),
      DeleteStatusModal({
        ...deleteStatusModal,
        closeDeleteModal,
        loadStatuses,
        statuses: listData.statuses
      })
    ]
  }
}
