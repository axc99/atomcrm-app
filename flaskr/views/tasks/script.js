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
        completed: task.completed
      })
    }

    return {
      key: task.id,
      color: task.color,
      title: task.name,
      extra: `${task.subtaskCount} ${task.subtaskCount == 1 ? strs['table_count_task'] : strs['table_count_subtasks']}`,
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
  const [subtasks, setSubtasks] = useState([])

  useEffect(() => {
    if (opened) {
      if (task) {
        form.setFieldsValue({
          name: task.name
        })
        setSubtasks(task.subtasks)
      } else {
        form.setFieldsValue({
          name: ''
        })
        setSubtasks([])
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
              name: values.name,
              tasks: subtasks
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
          },
          {
            '_com': 'Field.Custom',
            'label': strs['taskModal_form_subtasks'],
            'content':
              TaskModalSubtasks({
                subtasks,
                setSubtasks
              })
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

const TaskModalSubtasks = ({ subtasks, setSubtasks }) => {
  const addSubtask = () => {
    subtasks.push({
      name: ''
    })
    setSubtasks([...subtasks])
  }

  const updateSubtask = (i, subtask) => {
    subtasks[i] = subtask
    setSubtasks([...subtasks])
  }

  const removeSubtask = (i) => {
    subtasks.splice(i, 1)
    setSubtasks([...subtasks])
  }

  const moveSubtask = (oldIndex, newIndex) => {
    subtasks.splice(newIndex, 0, subtasks.splice(oldIndex, 1)[0])
    setSubtasks([...subtasks])
  }

  const rows = subtasks.map((subtask, i) => ({
    name: {
      _com: 'Field.Input',
      value: subtask.name,
      onChange: ({ value }) => updateSubtask(i, { name: value })
    },
    actions: [
      {
        _com: 'Button',
        icon: 'delete',
        onClick: () => removeSubtask(i)
      }
    ]
  }))

  console.log('rows>>>', rows)

  return [
    {
      '_com': 'Table',
      'draggable': true,
      'emptyText': strs['taskModal_form_subtasks_table_noSubtasks'],
      'onDrag': ({ oldIndex, newIndex }) => moveSubtask(oldIndex, newIndex),
      'columns': [
          {
              'width': 35,
              'key': 'name'
          }
      ],
      'rows': rows
    },
    {
      '_com': 'Button',
      'label': strs['taskModal_form_subtasks_addSubtask'],
      'icon': 'plus',
      'type': 'solid',
      'onClick': () => addSubtask()
    }
  ]
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
  const deleteTask = ({ id, completed }) => {
    if (completed) {
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
