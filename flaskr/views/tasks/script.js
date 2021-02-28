const { React, moment, com } = window.globalEnv
const { view, app } = window.localEnv
const { useState, useEffect, useMemo } = React

const { useForm } = com.Form
const { strs, taskColors } = view.data

const TasksList = ({ tasks, deleteLoadingIndex, loading, openModal, deleteTask, onDragTask }) => {
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
          label: strs['table_editTask'],
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
    emptyText: strs['table_noTasks'],
    onDrag: onDragTask,
    items
  }
}

const TaskModal = ({ opened=false, type, closeModal, task, loadTasks }) => {
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
    title: type === 'create' ? strs['taskModal_createTitle'] : strs['taskModal_updateTitle'],
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
            label: strs['taskModal_form_name'],
            placeholder: strs['taskModal_form_name_placeholder'],
            maxLength: 30,
            rules: [
              {max: 30, message: strs['taskModal_form_name_length']},
              {required: true, message: strs['taskModal_form_name_required']}
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
            label: type === 'create' ? strs['taskModal_form_create'] : strs['taskModal_form_save']
          }
        ]
    }
    ]
  }
}

const DeleteTaskModal = ({ id, opened, closeDeleteModal, loadTasks, tasks }) => {
  const [reqLoading, setReqLoading] = useState(false)

  return {
    _com: 'Modal',
    title: strs['deleteTaskModal_title'],
    subtitle: strs['deleteTaskModal_subtitle'],
    buttons: [
       {
          _com: 'Button',
          type: 'danger',
          icon: 'delete',
          label: 'Delete',
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

view.render = () => {
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

  return {
    header: {
      title: strs['name'],
      count: listData.tasks.length,
      actions: [
        {
          _com: 'Button',
          label: strs['header_createTask'],
          type: 'primary',
          icon: 'plus',
          onClick: () => openModal({ type: 'create' })
        }
      ]
    },
    scheme: [
      TasksList({
        ...listData,
        openModal,
        onDragTask,
        deleteTask
      }),
      TaskModal({
        ...taskModal,
        loadTasks,
        closeModal
      }),
      DeleteTaskModal({
        ...deleteTaskModal,
        closeDeleteModal,
        loadTasks,
        tasks: listData.tasks
      })
    ]
  }
}
