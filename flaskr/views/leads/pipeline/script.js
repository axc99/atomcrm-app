const { React, moment, com } = window.globalEnv
const { view, app } = window.localEnv
const { useState, useEffect, useMemo } = React

const { useForm } = com.Form
const { strs, statusColors, statuses, filterParams, filterUsed, search, installationCardSettings, hasAnyIntegration, autocreateCategoryId } = view.data

const LeadModal = ({ opened, id, uid, closeLeadModal, loadLeads }) => {
  const [form] = useForm()
  const formFields = []
  const statusOptions = []
  const [reqLoading, setReqLoading] = useState(false)
  const [archiveReqLoading, setArchiveReqLoading] = useState(false)
  const [data, setData] = useState({
    lead: null,
    loading: true
  })

  useEffect(() => {
    if (opened) {
      loadLead()
    }
  }, [opened])

  if (data.lead) {
    data.lead.fields.map(field => {
      if (field['fieldValueType'] === 'boolean') {
        formFields.push({
          '_com': 'Field.Checkbox',
          'columnWidth': 12,
          'key': field.fieldId,
          'text': field.fieldName
        })
      } else if (field['fieldValueType'] === 'long_string') {
        formFields.push({
          '_com': 'Field.Input',
          'columnWidth': 12,
          'multiline': true,
          'key': field.id,
          'label': field.fieldName
        })
      } else if (field['fieldValueType'] === 'number') {
        formFields.push({
          '_com': 'Field.Input',
          'type': 'number',
          'columnWidth': 6,
          'key': field.fieldId,
          'label': field.fieldName
        })
      } else if (field['fieldValueType'] === 'date') {
        formFields.push({
          '_com': 'Field.DatePicker',
          'key': field.fieldId,
          'format': 'YYYY.MM.DD',
          'label': field.fieldName,
          'allowClear': true
        })
      } else if (field['fieldValueType'] === 'choice') {
        const choiceOptions = []

        formFields.push({
          '_com': 'Field.Select',
          'key': field.id,
          'label': field.fieldName,
          'options': choiceOptions
        })
      } else if (field['fieldValueType'] === 'phone') {
        formFields.push({
          '_com': 'Field.Input',
          'key': field.fieldId,
          'type': 'text',
          'columnWidth': 12,
          'label': field.fieldName,
          'rules': [
              {'pattern': /^[+]*[(]{0,1}[0-9]{1,3}[)]{0,1}[-\s\./0-9]*$/g, 'message': strs['v_updateLead_rule_phone']}
          ]
        })
      } else if (field['fieldValueType'] === 'email') {
        formFields.push({
          '_com': 'Field.Input',
          'key': field.fieldId,
          'type': 'text',
          'columnWidth': 12,
          'label': field.fieldName,
          'rules': [
              {'pattern': /\S+@\S+\.\S+/, 'message': strs['v_updateLead_rule_email']},
          ]
        })
      } else {
        formFields.push({
          '_com': 'Field.Input',
          'key': field.fieldId,
          'type': 'text',
          'columnWidth': 12,
          'label': field.fieldName
        })
      }
    })
  }

  statuses.map(status => {
    statusOptions.push({
      value: status.id,
      label: status.name,
      color: status.colorHex
    })
  })

  const loadLead = () => {
    app
      .sendReq('getLead', { id })
      .then(result => {
        if (result.res === 'ok') {
          const { lead } = result

          data.lead = lead
          data.lead.originalStatusId = lead.statusId

          setData({ ...data })

          const fieldsValue = {}
          data.lead.fields.map(field => {
            fieldsValue[field.fieldId] = field.value
          })
          form.setFieldsValue(fieldsValue)
        }
      })
  }

  const archiveLead = () => {
    setArchiveReqLoading(true)
    app
      .sendReq('archiveLead', { id })
      .then(result => {
        setArchiveReqLoading(false)

        if (result.res == 'ok') {
          data.lead.archived = true
          setData({ ...data })

          loadLeads({ statusId: data.lead.statusId })
        }
      })
  }

  const restoreLead = () => {
    setArchiveReqLoading(true)
    app
      .sendReq('restoreLead', { id })
      .then(result => {
        setArchiveReqLoading(false)

        if (result.res == 'ok') {
          data.lead.archived = false
          setData({ ...data })

          loadLeads({ statusId: data.lead.statusId })
        }
      })
  }

//  currency = self.installation_card_settings.getCurrency()
  const amountPrefix = 111 // currency['format_string'].split('{}')[0]
  const amountSuffix = 222 // currency['format_string'].split('{}')[1]

  console.log('data.lead && data.lead.statusId', data.lead && data.lead.statusId)

  return {
    _com: 'Modal',
    size: 'medium',
    opened,
    title: 'title',
    onCancel: () => closeLeadModal(),
    content: [
      {
        '_com': 'Grid',
        'columns': [
          {
            'span': 12,
            'sm': 7,
            'content': [
              {
                _com: 'Form',
                form,
                onFinish: ({ values }) => {
                  const fields = []
                  Object.entries(values).map(([key, value]) => {
                    fields.push({
                      fieldId: +key,
                      value: value
                    })
                  })

                  setReqLoading(true)
                  app
                    .sendReq('updateLead', {
                      id,
                      fields,
                      tags: data.lead.tags,
                      amount: data.lead.amount,
                      comment: data.lead.comment,
                      statusId: data.lead.statusId
                    })
                    .then(result => {
                      setReqLoading(false)

                      if (result.res == 'ok') {
                        if (data.lead.statusId != data.lead.originalStatusId) {
                          loadLeads({ statusId: data.lead.statusId })
                          loadLeads({ statusId: data.lead.originalStatusId })
                        } else {
                          loadLeads({ statusId: data.lead.statusId })
                        }

                        app.showNotification({
                          message: 'SAVING_NOTIFICATION_MESSAGE',
                          duration: 1
                        })
                      }
                    })
                },
                'fields': formFields,
                'buttons': [
                  {
                    '_com': 'Button',
                    'type': 'primary',
                    'submitForm': true,
                    'loading': reqLoading,
                    'icon': 'save',
                    'label': strs['v_updateLead_save']
                  },

                  (data.lead && (!data.lead.archived ? {
                    '_com': 'Button',
                    'icon': 'delete',
                    'loading': archiveReqLoading,
                    'onClick': () => archiveLead()
                  } : {
                    '_com': 'Button',
                    'icon': 'reload',
                    'type': 'solid',
                    'loading': archiveReqLoading,
                    'label': strs['v_updateLead_restoreLead'],
                    'onClick': () => restoreLead()
                  }))
                ]
              }
            ]
          },
          {
            'span': 12,
            'sm': 5,
            'content': [
              {
                '_com': 'Area',
                'background': '#f9f9f9',
                'content': [
                  {
                    '_com': 'Field.Select',
                    'placeholder': 'Select status',
                    'value': data.lead && data.lead.statusId,
                    'options': statusOptions,
                    'onChange': ({ value }) => {
                      data.lead.statusId = value
                      setData({ ...data })
                    }
                  },
                  {
                    '_com': 'Field.Input',
                    '_id': 'updateLeadForm_amount',
                    '_vis': installationCardSettings.amountEnabled,
                    'type': 'number',
                    'prefix': amountPrefix,
                    'suffix': amountSuffix,
                    'min': 0,
                    'max': 10000000000,
                    'placeholder': '0',
                    'value': (data.lead && data.lead.amount) ? data.lead.amount : 0,
                    'onChange': ({ value }) => {
                      data.lead.amount = value
                      setData({ ...data })
                    }
                  },
                  {
                    '_com': 'Field.Input',
                    '_id': 'updateLeadForm_tags',
                    'multiple': true,
                    'value': data.lead && data.lead.tags,
                    'placeholder': strs['v_updateLead_enterTags'],
                    'onChange': ({ value }) => {
                      data.lead.tags = value
                      setData({ ...data })
                    }
                  },
                  {
                    '_com': 'Field.Input',
                    '_id': 'updateLeadForm_comment',
                    'multiline': true,
                    'maxLength': 500,
                    'value': data.lead && data.lead.comment,
                    'placeholder': strs['v_updateLead_enterComment'],
                    'onChange': ({ value }) => {
                      data.lead.comment = value
                      setData({ ...data })
                    }
                  },
                  {
                    '_com': 'Details',
                    'items': [
                      {
                        'label': strs['v_updateLead_addDate'],
                        'value': data.lead && data.lead.addDate,
//                        Lead.get_regular_date((self.lead.add_date + timedelta(
//                            minutes=request_data['timezone_offset'])).strftime(
//                            '%Y-%m-%d %H:%M:%S'))
                      },
                      {
                        'label': strs['v_updateLead_updateDate'],
                        'value': data.lead && data.lead.updDate
//                        Lead.get_regular_date((self.lead.upd_date + timedelta(
//                            minutes=request_data['timezone_offset'])).strftime(
//                            '%Y-%m-%d %H:%M:%S'))
                      },
                      data.lead && data.lead.nepkitUserId && {
                        'label': strs['v_updateLead_creator'],
                        'value': {
                            '_com': 'User',
                            'userId': data.lead.nepkitUserId
                        }
                      }
                    ]
                  },
//                  {
//                      '_com': 'Details',
//                      'title': _('v_updateLead_utmMarks'),
//                      'items': [
//                          {'label': 'utm_source',
//                           'value': self.lead.utm_source} if self.lead.utm_source else None,
//                          {'label': 'utm_medium',
//                           'value': self.lead.utm_medium} if self.lead.utm_medium else None,
//                          {'label': 'utm_campaign',
//                           'value': self.lead.utm_campaign} if self.lead.utm_campaign else None,
//                          {'label': 'utm_term',
//                           'value': self.lead.utm_term} if self.lead.utm_term else None,
//                          {'label': 'utm_content',
//                           'value': self.lead.utm_content} if self.lead.utm_content else None
//                      ]
//                  } if (
//                          self.lead.utm_source or
//                          self.lead.utm_medium or
//                          self.lead.utm_campaign or
//                          self.lead.utm_term or
//                          self.lead.utm_content
//                  ) else None
                ]
              }
            ]
          }
        ]
      }
    ]
  }
}

const FilterModal = ({ opened, closeFilterModal }) => {
  const [form] = useForm()

  useEffect(() => {
    form.setFieldsValue({
      period: [
        filterParams['periodFrom'] && moment(filterParams['periodFrom'], 'YYYY.MM.DD'),
        filterParams['periodTo'] && moment(filterParams['periodTo'], 'YYYY.MM.DD')
      ],
      utmSource: filterParams['utmSource'],
      utmMedium: filterParams['utmMedium'],
      utmCampaign: filterParams['utmCampaign'],
      utmTerm: filterParams['utmTerm'],
      utmContent: filterParams['utmContent'],
      archived: filterParams['archived']
    })
  }, [filterParams])

  return {
    _com: 'Modal',
    opened,
    title: 'title',
    content: [
      {
        _com: 'Form',
        form,
        onFinish: ({ values }) => {
          app
            .getPage()
            .to({
              periodFrom: (values['period'][0] && values['period'][0].format('YYYY.MM.DD')) || '',
              periodTo: (values['period'][1] && values['period'][1].format('YYYY.MM.DD')) || '',
              utmSource: values['utmSource'] || '',
              utmMedium: values['utmMedium'] || '',
              utmCampaign: values['utmCampaign'] || '',
              utmTerm: values['utmTerm'] || '',
              utmContent: values['utmContent'] || '',
              archived: values['archived'] || ''
            })

          closeFilterModal()
        },
        fields: [
          {
            '_com': 'Field.DatePicker',
            'key': 'period',
            'label': strs['schema_form_period'],
            'columnWidth': 12,
            'range': true,
            'allowClear': true,
            'format': 'YYYY.MM.DD'
          },
          {
            '_com': 'Field.Input',
            'key': 'utmSource',
            'columnWidth': 6,
            'label': 'UTM source'
          },
          {
            '_com': 'Field.Input',
            'key': 'utmMedium',
            'columnWidth': 6,
            'label': 'UTM medium'
          },
          {
            '_com': 'Field.Input',
            'key': 'utmCampaign',
            'columnWidth': 6,
            'label': 'UTM campaign'
          },
          {
            '_com': 'Field.Input',
            'key': 'utmTerm',
            'columnWidth': 6,
            'label': 'UTM term'
          },
          {
            '_com': 'Field.Input',
            'key': 'utmContent',
            'columnWidth': 6,
            'label': 'UTM content'
          },
          {
            '_com': 'Field.Checkbox',
            'key': 'archived',
            'text': strs['schema_form_archivedLeads']
          }
        ],
        buttons: [
          {
            '_com': 'Button',
            'icon': 'check',
            'submitForm': true,
            'type': 'primary',
            'label': strs['schema_form_apply']
          },
          {
            '_com': 'Button',
            'label': strs['schema_form_clear'],
            'onClick': 'onClickClear'
          }
        ]
      }
  ],
    onCancel: () => closeFilterModal()
  }
}


view.render = () => {
  const [data, setData] = useState({
    statuses: [],
    loading: true,
    loadingColIndex: null,
    addLoadingColIndex: null
  })
  const [filterModal, setFilterModal] = useState({
    opened: false
  })
  const [leadModal, setLeadModal] = useState({
    id: null,
    uid: null,
    opened: false
  })

  const boardColumns = []
  data.statuses.map((status, i) => {
    const boardColumnItems = status.leads.map(lead => {
      let title = ''
      let description = []

      console.log('lead.fields-->', lead.fields)

      lead.fields.map(field => {
        if (field['value'] && ['string', 'number', 'date'].includes(field['fieldValueType'])) {
          if (field['fieldBoardVisibility'] === 'title') {
            title += field['value'] + ' '
          } else if (field['fieldBoardVisibility'] === 'subtitle') {
            description.push(field['value'])
          }
        }
      })

      const extra = [lead['archived'] ? 'Archived' : lead['add_date']]
      if (installationCardSettings['amountEnabled'] && lead['amount']) {
        extra.unshift(lead['amount'])
      }

      title = title.trim()

      return {
        key: lead['id'],
        title: title || `#${lead['uid']}`,
        description,
        extra: extra,
        order: lead['id'],
        onClick: () => {
          openLeadModal({
            id: lead['id'],
            uid: lead['uid']
          })
        }
      }
    })
    boardColumns.push({
      'key': status['id'],
      'title': status['name'],
      'subtitle': installationCardSettings['amountEnabled'] && status['leadAmountSumStr'],
      'color': status['colorHex'],
      'items': boardColumnItems,
      'loading': data.loadingColIndex === i,
      'addLoading': data.addLoadingColIndex === i,
      'showAdd': !(filterUsed || search),
      'onAdd': () => {
        createLead({
          statusId: status.id
        })
      },
      'total': status['leadTotal'],
      'loadLimit': 10,
      'onLoad': () => {
        loadLeads({
          statusId: status.id,
          addToEnd: true
        })
      }
//      'onLoad': ['loadLeads', {
//          'statusId': status['id'],
//          'addToEnd': true
//      }]
    })
  })

  useEffect(() => {
    statuses.map(status => {
      data.statuses.push({
        ...status,
        leads: [],
        leadTotal: 0,
        leadAmountSumStr: 0
      })
    })

    setData({ ...data })
  }, [statuses])

  useEffect(() => {
    data.statuses.map(status => {
      loadLeads({
        statusId: status.id
      })
    })
  }, [data.statuses])

  // Open filter modal
  const openFilterModal = () => {
    setFilterModal({
      opened: true
    })
  }

  // Close filter modal
  const closeFilterModal = () => {
    setFilterModal({
      opened: false
    })
  }

  // Open lead modal
  const openLeadModal = ({ id, uid }) => {
    setLeadModal({
      id,
      uid,
      opened: true
    })
  }

  // Close lead modal
  const closeLeadModal = () => {
    setLeadModal({
      opened: false
    })
  }

  const createLead = ({ statusId }) => {
    const addLoadingColIndex = statuses.findIndex(status => status.id === statusId)
    setData({
      ...data,
      addLoadingColIndex
    })

    app
      .sendReq('createLead', {
        statusId
      })
      .then(result => {
        if (result.res === 'ok') {
          app
            .sendReq('getLeads', {
              statusId,
              offset: 0,
              limit: 10,
              search: '',
              filter: {}
            })
            .then(result => {
              if (result.res == 'ok') {
                const { leads, leadTotal, leadAmountSum, leadAmountSumStr } = result
                const status = data.statuses.find(s => s.id === statusId)

                status.leads = leads
                status.leadTotal = leadTotal
                status.leadAmountSum = leadAmountSum
                status.leadAmountSumStr = leadAmountSumStr

                setData({
                  ...data,
                  addLoadingColIndex: null
                })
              }
            })
        }
      })
  }

  const loadLeads = ({ statusId, addToEnd=false }) => {
    const colIndex = data.statuses.findIndex(status => status.id === statusId)
    setData({
      ...data,
      loadingColIndex: colIndex
    })

    app
      .sendReq('getLeads', {
        statusId,
        offset: addToEnd ? data.statuses[colIndex].leads.length : 0,
        limit: (addToEnd || data.statuses[colIndex].leads.length < 10) ? 10 : data.statuses[colIndex].leads.length,
        search: '',
        filter: {}
      })
      .then(result => {
        if (result.res === 'ok') {
          const { leads, leadTotal, leadAmountSum, leadAmountSumStr } = result
          const status = data.statuses.find(s => s.id === statusId)

          status.leads = !addToEnd ? leads : [ ...status.leads, ...leads ]
          status.leadTotal = leadTotal
          status.leadAmountSum = leadAmountSum
          status.leadAmountSumStr = leadAmountSumStr

          setData({
            ...data,
            loadingColIndex: null
          })

//              // Set total and set/append items
//              boardColumns[columnIndex].total = leadTotal
//              if (leadAmountSumStr) {
//                  boardColumns[columnIndex].subtitle = leadAmountSumStr
//              }
//              boardColumns[columnIndex].items = !addToEnd ? leadComponents : [
//                  ...boardColumns[columnIndex].items,
//                  ...leadComponents
//              ]
//
//              board.setAttr('columns', boardColumns)
        }
      })
  }

  useEffect(() => {
    if (statuses) {
      statuses.map(status => {
        loadLeads({
          statusId: status.id
        })
      })
    }
  }, [statuses])

  return {
    header: {
      'title': strs['schema_header_title'],
      'actions': [
        !hasAnyIntegration && {
          '_com': 'Button',
          'type': 'solid',
          'icon': 'plusCircle',
          'label': strs['v_pipeline_header_autoCreate'],
          'to': ['control', {
              'tab': 'extensions',
              'category': autocreateCategoryId
          }]
        },
        {
          '_com': 'Button',
          'icon': 'filter',
          'label': 'Filter',
          'onClick': () => openFilterModal(),
          'dot': filterUsed
        }
      ],
      'search': {
        'value': search,
        'placeholder': 'v_pipeline_header_search',
        'onSearch': ({ value }) => {
          app
            .getPage()
            .to({
                search: value
            })
        }
      }
    },
    schema: [
      {
        _com: 'Board',
        draggableBetweenColumns: true,
        onDrag: ({ key, oldColumnIndex, newColumnIndex, newColumnKey, oldItemIndex, newItemIndex }) => {
          // Get item from old column
          const item = data.statuses[oldColumnIndex].leads[oldItemIndex]
          // Remove item from column
          data.statuses[oldColumnIndex].leads.splice(oldItemIndex, 1)
          // Add item new column
          data.statuses[newColumnIndex].leads.splice(newItemIndex, 0, item)
          // Sort by order attr
          data.statuses[newColumnIndex].leads.sort((a, b) => a.order < b.order)

          setData({ ...data })

          app
            .sendReq('updateLeadStatus', {
              id: key,
              statusId: +newColumnKey
            })
            .then(result => {
              loadLeads({ statusId: data.statuses[oldColumnIndex].id })
              loadLeads({ statusId: data.statuses[newColumnIndex].id })
            })
        },
        columns: boardColumns
      },
      FilterModal({
        ...filterModal,
        closeFilterModal
      }),
      LeadModal({
        ...leadModal,
        closeLeadModal,
        loadLeads,
        statuses: data.statuses
      })
    ]
  }
}
