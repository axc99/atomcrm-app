var _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; };

const { React, moment, com } = window.globalEnv;
const { view, app } = window.localEnv;
const { useState, useEffect, useMemo } = React;

const { useForm } = com.Form;
const { strs, statusColors, statuses, filterParams, filterUsed, search, installationCardSettings, hasAnyIntegration, autocreateCategoryId } = view.data;

const todayObj = new Date();
todayObj.setHours(0, 0, 0, 0);

const yesterdayObj = new Date();
yesterdayObj.setDate(yesterdayObj.getDate() - 1);
yesterdayObj.setHours(0, 0, 0, 0);

const getRegularDate = srcDate => {
  const [date, time] = srcDate.split(' ');
  const [year, month, day] = date.split('-');
  const [hours, minutes, seconds] = time.split(':');

  const dateObj = new Date(date);
  dateObj.setHours(0, 0, 0, 0);

  const months = {
    '01': strs['getRegularDate_jan'],
    '02': strs['getRegularDate_feb'],
    '03': strs['getRegularDate_mar'],
    '04': strs['getRegularDate_apr'],
    '05': strs['getRegularDate_may'],
    '06': strs['getRegularDate_jun'],
    '07': strs['getRegularDate_jul'],
    '08': strs['getRegularDate_aug'],
    '09': strs['getRegularDate_sep'],
    '10': strs['getRegularDate_oct'],
    '11': strs['getRegularDate_nov'],
    '12': strs['getRegularDate_dec']
  };
  const monthStr = months[month];

  if (dateObj.getTime() === todayObj.getTime()) {
    return strs['getRegularDate_today'].replace('{time}', `${hours}:${minutes}`);
  } else if (dateObj.getTime() === yesterdayObj.getTime()) {
    return strs['getRegularDate_yesterday'].replace('{time}', `${hours}:${minutes}`);
  } else {
    if (year == dateObj.getFullYear()) {
      return `${day} ${monthStr}`.replace('{time}', `${hours}:${minutes}`);
    } else {
      return `${day} ${monthStr} ${year}`.replace('{time}', `${hours}:${minutes}`);
    }
  }

  return date;
};

const LeadModal = ({ opened, id, uid, closeLeadModal, loadLeads }) => {
  const [form] = useForm();
  const formFields = [];
  const statusOptions = [];
  const [reqLoading, setReqLoading] = useState(false);
  const [archiveReqLoading, setArchiveReqLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('information');
  const [data, setData] = useState({
    lead: null,
    loading: true
  });

  useEffect(() => {
    if (opened) {
      setActiveTab('information');
      loadLead();
    }
  }, [opened]);

  if (data.lead) {
    data.lead.fields.map(field => {
      if (field['fieldValueType'] === 'boolean') {
        formFields.push({
          '_com': 'Field.Checkbox',
          'columnWidth': 12,
          'key': field.fieldId,
          'text': field.fieldName
        });
      } else if (field['fieldValueType'] === 'long_string') {
        formFields.push({
          '_com': 'Field.Input',
          'columnWidth': 12,
          'multiline': true,
          'key': field.id,
          'label': field.fieldName
        });
      } else if (field['fieldValueType'] === 'number') {
        formFields.push({
          '_com': 'Field.Input',
          'type': 'number',
          'columnWidth': 6,
          'key': field.fieldId,
          'label': field.fieldName
        });
      } else if (field['fieldValueType'] === 'date') {
        formFields.push({
          '_com': 'Field.DatePicker',
          'key': field.fieldId,
          'format': 'YYYY.MM.DD',
          'label': field.fieldName,
          'allowClear': true
        });
      } else if (field['fieldValueType'] === 'choice') {
        const choiceOptions = [];

        if (field['choiceOptions']) {
          Object.entries(field['choiceOptions']).map(([optionKey, optionValue]) => {
            choiceOptions.push({
              value: optionKey,
              label: optionValue
            });
          });
        }

        formFields.push({
          '_com': 'Field.Select',
          'key': field.fieldId,
          'placeholder': strs['leadModal_select_selectOption'],
          'label': field.fieldName,
          'options': choiceOptions
        });
      } else if (field['fieldValueType'] === 'phone') {
        formFields.push({
          '_com': 'Field.Input',
          'key': field.fieldId,
          'type': 'text',
          'columnWidth': 12,
          'label': field.fieldName,
          'rules': [{ 'pattern': /^[+]*[(]{0,1}[0-9]{1,3}[)]{0,1}[-\s\./0-9]*$/g, 'message': strs['leadModal_form_phone_rule'] }]
        });
      } else if (field['fieldValueType'] === 'email') {
        formFields.push({
          '_com': 'Field.Input',
          'key': field.fieldId,
          'type': 'text',
          'columnWidth': 12,
          'label': field.fieldName,
          'rules': [{ 'pattern': /\S+@\S+\.\S+/, 'message': strs['leadModal_form_email_rule'] }]
        });
      } else {
        formFields.push({
          '_com': 'Field.Input',
          'key': field.fieldId,
          'type': 'text',
          'columnWidth': 12,
          'label': field.fieldName
        });
      }
    });
  }

  statuses.map(status => {
    statusOptions.push({
      value: status.id,
      label: status.name,
      color: status.colorHex
    });
  });

  const loadLead = () => {
    setData(_extends({}, data, {
      loading: true
    }));

    app.sendReq('getLead', { id }).then(result => {
      if (result.res === 'ok') {
        const { lead } = result;

        data.lead = lead;
        data.lead.originalStatusId = lead.statusId;

        setData(_extends({}, data, {
          loading: false
        }));

        const fieldsValue = {};
        data.lead.fields.map(field => {
          fieldsValue[field.fieldId] = field.value;
        });

        form.setFieldsValue(fieldsValue);
      }
    });
  };

  const archiveLead = () => {
    setArchiveReqLoading(true);
    app.sendReq('archiveLead', { id }).then(result => {
      setArchiveReqLoading(false);

      if (result.res == 'ok') {
        data.lead.archived = true;
        setData(_extends({}, data));

        loadLeads({ statusId: data.lead.statusId });
      }
    });
  };

  const restoreLead = () => {
    setArchiveReqLoading(true);
    app.sendReq('restoreLead', { id }).then(result => {
      setArchiveReqLoading(false);

      if (result.res == 'ok') {
        data.lead.archived = false;
        setData(_extends({}, data));

        loadLeads({ statusId: data.lead.statusId });
      }
    });
  };

  return {
    _com: 'Modal',
    size: 'medium',
    loading: data.loading,
    opened,
    title: strs['leadModal_title'].replace('{id}', uid),
    tabs: [{
      'text': strs['leadModal_tabs_information'],
      'key': 'information',
      'active': activeTab === 'information'
    }, data.lead && data.lead.taskCount > 0 && {
      'text': strs['leadModal_tabs_tasks'],
      'key': 'tasks',
      'active': activeTab === 'tasks'
    }, {
      'text': strs['leadModal_tabs_activity'],
      'key': 'activity',
      'active': activeTab === 'activity'
    }],
    onChangeTab: ({ key }) => setActiveTab(key),
    onCancel: () => closeLeadModal(),
    content: [{
      'information': LeadModalInformation({
        form,
        formFields,
        statusOptions,
        reqLoading,
        setReqLoading,
        archiveReqLoading,
        setArchiveReqLoading,
        data,
        setData,
        loadLeads
      }),
      'tasks': LeadModalTasks({
        data,
        setData
      }),
      'activity': LeadModalActivity({
        data,
        setData,
        opened: activeTab === 'activity'
      })
    }[activeTab]]
  };
};

const LeadModalInformation = ({
  form,
  formFields,
  statusOptions,
  reqLoading,
  setReqLoading,
  archiveReqLoading,
  setArchiveReqLoading,
  data,
  setData,
  loadLeads
}) => {
  const currency = installationCardSettings.currency;
  const [amountPrefix, amountSuffix] = currency.formatString.split('{}');

  return {
    '_com': 'Grid',
    'columns': [{
      'span': 12,
      'sm': 7,
      'content': [{
        _com: 'Form',
        form,
        onFinish: ({ values }) => {
          const fields = [];
          Object.entries(values).map(([key, value]) => {
            fields.push({
              fieldId: +key,
              value: value
            });
          });

          setReqLoading(true);
          app.sendReq('updateLead', {
            id: data.lead.id,
            fields,
            tags: data.lead.tags,
            comment: data.lead.comment,
            amount: +data.lead.amount,
            statusId: +data.lead.statusId
          }).then(result => {
            setReqLoading(false);

            if (result.res == 'ok') {
              if (data.lead.statusId != data.lead.originalStatusId) {
                loadLeads({ statusId: data.lead.statusId });
                loadLeads({ statusId: data.lead.originalStatusId });
              } else {
                loadLeads({ statusId: data.lead.statusId });
              }

              app.showNotification({
                message: strs['leadModal_notification_changesSaved'],
                duration: 1
              });
            }
          });
        },
        'fields': formFields,
        'buttons': [{
          '_com': 'Button',
          'type': 'primary',
          'submitForm': true,
          'loading': reqLoading,
          'icon': 'save',
          'label': strs['leadModal_form_save']
        }, data.lead && (!data.lead.archived ? {
          '_com': 'Button',
          'icon': 'delete',
          'loading': archiveReqLoading,
          'onClick': () => archiveLead()
        } : {
          '_com': 'Button',
          'icon': 'reload',
          'type': 'solid',
          'loading': archiveReqLoading,
          'label': strs['leadModal_form_restoreLead'],
          'onClick': () => restoreLead()
        })]
      }]
    }, {
      'span': 12,
      'sm': 5,
      'content': [{
        '_com': 'Area',
        'backgroundColor': '#f9f9f9',
        'content': [{
          '_com': 'Field.Select',
          'value': data.lead && data.lead.statusId,
          'options': statusOptions,
          'onChange': ({ value }) => {
            data.lead.statusId = value;
            setData(_extends({}, data));
          }
        }, {
          '_com': 'Field.Input',
          '_id': 'updateLeadForm_amount',
          '_vis': installationCardSettings.amountEnabled,
          'type': 'number',
          'prefix': amountPrefix,
          'suffix': amountSuffix,
          'min': 0,
          'max': 10000000000,
          'placeholder': '0',
          'value': data.lead && data.lead.amount ? data.lead.amount : 0,
          'onChange': ({ value }) => {
            data.lead.amount = value;
            setData(_extends({}, data));
          }
        }, {
          '_com': 'Field.Input',
          'multiple': true,
          'value': data.lead && data.lead.tags,
          'placeholder': strs['leadModal_tags'],
          'onChange': ({ value }) => {
            data.lead.tags = value;
            setData(_extends({}, data));
          }
        }, {
          '_com': 'Field.Input',
          'multiline': true,
          'maxLength': 500,
          'value': data.lead && data.lead.comment,
          'placeholder': strs['leadModal_comment'],
          'onChange': ({ value }) => {
            data.lead.comment = value;
            setData(_extends({}, data));
          }
        }, {
          '_com': 'Details',
          'items': [{
            'label': strs['leadModal_addDate'],
            'value': data.lead && getRegularDate(data.lead.addDate)
          }, {
            'label': strs['leadModal_updateDate'],
            'value': data.lead && getRegularDate(data.lead.updDate)
          }, data.lead && data.lead.nepkitUserId && {
            'label': strs['leadModal_creator'],
            'value': {
              '_com': 'User',
              'userId': data.lead.nepkitUserId
            }
          }]
        }, data.lead && data.lead.utmSource && data.lead.utmMedium && data.lead.utmCampaign && data.lead.utmTerm && data.lead.utmContent && {
          '_com': 'Details',
          'title': strs['leadModal_utmMarks'],
          'items': [data.lead.utmSource && { 'label': 'utm_source',
            'value': data.lead.utmSource }, data.lead.utmMedium && { 'label': 'utm_medium',
            'value': data.lead.utmMedium }, data.lead.utmCampaign && { 'label': 'utm_campaign',
            'value': data.lead.utmCampaign }, data.lead.utmTerm && { 'label': 'utm_term',
            'value': data.lead.utmTerm }, data.lead.utmContent && { 'label': 'utm_content',
            'value': data.lead.utmContent }]
        }]
      }]
    }]
  };
};

const LeadModalTasks = ({ data, setData }) => {
  const checkedKeys = [];
  const tasksItems = data.lead && data.lead.tasks.map(task => {
    if (task.completed) {
      checkedKeys.push(task.id);
    }

    return {
      'title': task.name,
      'key': task.id,
      'children': task.subtasks && task.subtasks.map(subtask => {
        if (subtask.completed) {
          checkedKeys.push(subtask.id);
        }

        return {
          'title': subtask.name,
          'key': subtask.id
        };
      })
    };
  });

  return {
    '_com': 'Form',
    '_id': 'updateLeadForm',
    'fields': [{
      '_com': 'Field.Tree',
      'key': 'tasks',
      'items': tasksItems,
      'value': checkedKeys,
      'onChange': ({ value }) => {
        app.sendReq('completeLeadTasks', {
          id: data.lead.id,
          task_ids: value
        }).then(result => {
          if (result.res == 'ok') {
            data.lead.tasks.map(task => {
              task.completed = value.includes(task.id);

              if (task.subtasks) {
                task.subtasks.map(subtask => {
                  subtask.completed = value.includes(subtask.id);
                });
              }
            });
            console.log('data.lead.tasks', data.lead.tasks);
            setData(_extends({}, data));
          }
        });
      },
      'defaultExpandAll': true
    }]
  };
};

const LeadModalActivity = ({ data, opened }) => {
  const [activityData, setActivityData] = useState({
    actions: [],
    loading: true,
    page: 1
  });

  const loadActions = () => {
    const offset = (activityData.page - 1) * 10;
    const limit = 10;

    setActivityData(_extends({}, activityData, {
      loading: true
    }));

    app.sendReq('getLeadActions', {
      leadId: data.lead.id,
      offset,
      limit
    }).then(result => {
      if (result.res === 'ok') {
        const { actions, actionTotal } = result;

        setActivityData(_extends({}, activityData, {
          loading: false,
          actionTotal: actionTotal,
          actions
        }));
      }
    });
  };

  useEffect(() => {
    if (data.lead && opened) {
      loadActions();
    }
  }, [activityData.page, data.lead, opened]);

  const items = activityData.actions.map(action => {
    return {
      'title': action['title'],
      'color': action['color'],
      'extra': action['log_date']
    };
  });

  return {
    '_com': 'Timeline',
    'loading': activityData.loading,
    'page': activityData.page,
    'total': activityData.actionTotal,
    'onChangePage': ({ page }) => {
      setActivityData(_extends({}, activityData, {
        page
      }));
    },
    'pageSize': 10,
    'items': items
  };
};

const FilterModal = ({ opened, closeFilterModal }) => {
  const [form] = useForm();

  useEffect(() => {
    form.setFieldsValue({
      period: [filterParams['periodFrom'] && moment(filterParams['periodFrom'], 'YYYY.MM.DD'), filterParams['periodTo'] && moment(filterParams['periodTo'], 'YYYY.MM.DD')],
      utmSource: filterParams['utmSource'],
      utmMedium: filterParams['utmMedium'],
      utmCampaign: filterParams['utmCampaign'],
      utmTerm: filterParams['utmTerm'],
      utmContent: filterParams['utmContent'],
      archived: filterParams['archived']
    });
  }, [filterParams]);

  return {
    _com: 'Modal',
    opened,
    title: strs['filterModal_title'],
    onCancel: () => closeFilterModal(),
    content: [{
      _com: 'Form',
      form,
      onFinish: ({ values }) => {
        console.log('values', values);

        app.getView().to({
          periodFrom: values['period'][0] && values['period'][0].format('YYYY.MM.DD') || '',
          periodTo: values['period'][1] && values['period'][1].format('YYYY.MM.DD') || '',
          utmSource: values['utmSource'] || '',
          utmMedium: values['utmMedium'] || '',
          utmCampaign: values['utmCampaign'] || '',
          utmTerm: values['utmTerm'] || '',
          utmContent: values['utmContent'] || '',
          archived: values['archived'] || ''
        });

        closeFilterModal();
      },
      fields: [{
        '_com': 'Field.DatePicker',
        'key': 'period',
        'label': strs['filterModal_form_period'],
        'columnWidth': 12,
        'range': true,
        'allowClear': true,
        'format': 'YYYY.MM.DD'
      }, {
        '_com': 'Field.Input',
        'key': 'utmSource',
        'columnWidth': 6,
        'label': 'UTM source'
      }, {
        '_com': 'Field.Input',
        'key': 'utmMedium',
        'columnWidth': 6,
        'label': 'UTM medium'
      }, {
        '_com': 'Field.Input',
        'key': 'utmCampaign',
        'columnWidth': 6,
        'label': 'UTM campaign'
      }, {
        '_com': 'Field.Input',
        'key': 'utmTerm',
        'columnWidth': 6,
        'label': 'UTM term'
      }, {
        '_com': 'Field.Input',
        'key': 'utmContent',
        'columnWidth': 6,
        'label': 'UTM content'
      }, {
        '_com': 'Field.Checkbox',
        'key': 'archived',
        'text': strs['filterModal_form_archivedLeads']
      }],
      buttons: [{
        '_com': 'Button',
        'icon': 'check',
        'submitForm': true,
        'type': 'primary',
        'label': strs['filterModal_form_apply']
      }, {
        '_com': 'Button',
        'label': strs['filterModal_form_clear'],
        'onClick': () => {
          form.resetFields();
        }
      }]
    }]
  };
};

view.render = () => {
  const [data, setData] = useState({
    statuses: [],
    loading: false,
    loadingColIndex: null,
    addLoadingColIndex: null
  });
  const [filterModal, setFilterModal] = useState({
    opened: false
  });
  const [leadModal, setLeadModal] = useState({
    id: null,
    uid: null,
    opened: false
  });

  const boardColumns = [];
  data.statuses.map((status, i) => {
    const boardColumnItems = status.leads.map(lead => {
      let title = '';
      let description = [];

      lead.fields.map(field => {
        if (field['value'] && ['string', 'email', 'phone', 'number', 'date'].includes(field['fieldValueType'])) {
          if (field['fieldBoardVisibility'] === 'title') {
            title += field['value'] + ' ';
          } else if (field['fieldBoardVisibility'] === 'subtitle') {
            description.push(field['value']);
          }
        }
      });

      const extra = [lead['archived'] ? strs['board_archived'] : getRegularDate(lead['addDate'])];
      if (installationCardSettings['amountEnabled'] && lead['amount']) {
        extra.unshift(lead['amount']);
      }

      title = title.trim();
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
          });
        }
      };
    });
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
        });
      },
      'total': status['leadTotal'],
      'loadLimit': 10,
      'onLoad': () => {
        loadLeads({
          statusId: status.id,
          addToEnd: true
        });
      }
      //      'onLoad': ['loadLeads', {
      //          'statusId': status['id'],
      //          'addToEnd': true
      //      }]
    });
  });

  useEffect(() => {
    statuses.map(status => {
      data.statuses.push(_extends({}, status, {
        leads: [],
        inited: false,
        leadTotal: 0,
        leadAmountSumStr: 0
      }));
    });

    setData(_extends({}, data));

    data.statuses.map(status => {
      loadLeads({
        statusId: status.id
      });
    });

    setData(data => _extends({}, data, { loading: false }));
  }, [statuses]);

  // Open filter modal
  const openFilterModal = () => {
    setFilterModal({
      opened: true
    });
  };

  // Close filter modal
  const closeFilterModal = () => {
    setFilterModal({
      opened: false
    });
  };

  // Open lead modal
  const openLeadModal = ({ id, uid }) => {
    setLeadModal({
      id,
      uid,
      opened: true
    });
  };

  // Close lead modal
  const closeLeadModal = () => {
    setLeadModal({
      opened: false
    });
  };

  const createLead = ({ statusId }) => {
    const addLoadingColIndex = statuses.findIndex(status => status.id === statusId);
    setData(_extends({}, data, {
      addLoadingColIndex
    }));

    app.sendReq('createLead', {
      statusId
    }).then(result => {
      if (result.res === 'ok') {
        app.sendReq('getLeads', {
          statusId,
          offset: 0,
          limit: 10,
          search,
          filter: filterParams
        }).then(result => {
          if (result.res == 'ok') {
            const { leads, leadTotal, leadAmountSum, leadAmountSumStr } = result;
            const status = data.statuses.find(s => s.id === statusId);

            status.leads = leads;
            status.leadTotal = leadTotal;
            status.leadAmountSum = leadAmountSum;
            status.leadAmountSumStr = leadAmountSumStr;

            setData(_extends({}, data, {
              addLoadingColIndex: null
            }));
          }
        });
      }
    });
  };

  const loadLeads = ({ statusId, addToEnd = false }) => {
    const colIndex = data.statuses.findIndex(status => status.id === statusId);
    setData(_extends({}, data, {
      loadingColIndex: colIndex
    }));

    app.sendReq('getLeads', {
      statusId,
      offset: addToEnd ? data.statuses[colIndex].leads.length : 0,
      limit: addToEnd || data.statuses[colIndex].leads.length < 10 ? 10 : data.statuses[colIndex].leads.length,
      search,
      filter: filterParams
    }).then(result => {
      if (result.res === 'ok') {
        const { leads, leadTotal, leadAmountSum, leadAmountSumStr } = result;
        const status = data.statuses.find(s => s.id === statusId);

        status.leads = !addToEnd ? leads : [...status.leads, ...leads];
        status.leadTotal = leadTotal;
        status.leadAmountSum = leadAmountSum;
        status.leadAmountSumStr = leadAmountSumStr;
        status.inited = true;

        setData(data => _extends({}, data, {
          loadingColIndex: null
        }));
      }
    });
  };

  useEffect(() => {
    if (statuses) {
      statuses.map(status => {
        loadLeads({
          statusId: status.id
        });
      });
    }
  }, [statuses]);

  return {
    loading: data.loading,
    header: {
      'title': strs['header_title'],
      'actions': [{
        '_com': 'Button',
        'icon': 'filter',
        'label': strs['header_filter'],
        'onClick': () => openFilterModal(),
        'dot': filterUsed
      }, !hasAnyIntegration && {
        '_com': 'Button',
        'type': 'solid',
        'icon': 'plusCircle',
        'label': strs['header_autoCreate'],
        'to': ['control', {
          'tab': 'extensions',
          'category': autocreateCategoryId
        }]
      }],
      'search': {
        'value': search,
        'placeholder': strs['header_search'],
        'onSearch': ({ value }) => {
          app.getView().to({
            search: value
          });
        }
      }
    },
    scheme: [{
      _com: 'Board',
      draggableBetweenColumns: true,
      onDrag: ({ key, oldColumnIndex, newColumnIndex, newColumnKey, oldItemIndex, newItemIndex }) => {
        // Get item from old column
        const item = data.statuses[oldColumnIndex].leads[oldItemIndex];
        // Remove item from column
        data.statuses[oldColumnIndex].leads.splice(oldItemIndex, 1);
        // Add item new column
        data.statuses[newColumnIndex].leads.splice(newItemIndex, 0, item);
        // Sort by order attr
        data.statuses[newColumnIndex].leads.sort((a, b) => a.order < b.order);

        setData(_extends({}, data));

        app.sendReq('updateLeadStatus', {
          id: key,
          statusId: +newColumnKey
        }).then(result => {
          loadLeads({ statusId: data.statuses[oldColumnIndex].id });
          loadLeads({ statusId: data.statuses[newColumnIndex].id });
        });
      },
      columns: boardColumns
    }, FilterModal(_extends({}, filterModal, {
      closeFilterModal
    })), LeadModal(_extends({}, leadModal, {
      closeLeadModal,
      loadLeads,
      statuses: data.statuses
    }))]
  };
};