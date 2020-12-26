const { React, moment, com } = window.globalEnv
const { view, app } = window.localEnv
const { useState, useEffect, useMemo } = React

const { useForm } = com.Form
const { strs, statusColors } = view.data

view.render = () => {
  const [form] = useForm()

  const table_rows = []

  return {
    header: {
      title: strs['name']
    },
    schema: [
      {
        _com: 'Form',
        form,
        onFinish: () => {
          // ...
        },
        fields: [
          {
            '_com': 'Field.Checkbox',
            'key': 'amountEnabled',
            'text': strs['v_card_scheme_form_leadAmount'],
            'value': self.installation_card_settings.amount_enabled,
            'onChange': 'onChangeAmountEnabled'
          },
          {
            '_com': 'Field.Select',
            'key': 'currency',
            'withSearch': True,
            'disabled': not self.installation_card_settings.amount_enabled,
            'label': strs['v_card_scheme_form_amountCurrency'],
            'value': self.installation_card_settings.currency.name,
            'options': self.currency_options
          },
          {
            '_com': 'Field.Custom',
            '_id': 'updateCardSettingsForm_fields',
            'columnWidth': 12,
            'label': _('v_card_scheme_form_fields'),
            'content': [
              {
                '_com': 'Table',
                '_id': 'updateCardSettingsForm_fields_table',
                'draggable': True,
                'emptyText': _('v_card_scheme_form_fields_table_noFields'),
                'onDrag': 'onDragFields',
                'columns': [
                  {
                    'width': 35,
                    'key': 'name',
                    'title': _('v_card_scheme_form_fields_table_field')
                  },
                  {
                    'width': 35,
                    'key': 'valueType',
                    'title': _('v_card_scheme_form_fields_table_valueType')
                  },
                  {
                    'width': 30,
                    'key': 'boardVisibility',
                    'title': _('v_card_scheme_form_fields_table_boardVisibility')
                  }
                ],
                'rows': table_rows
              },
              {
                '_com': 'Button',
                '_id': 'updateCardSettingsForm_fields_addBtn',
                'label': _('v_card_scheme_form_fields_addField'),
                'icon': 'plus',
                'type': 'solid',
                'onClick': 'onClickAddField'
              }
            ]
          }
        ],
        buttons: [
          {
            '_com': 'Button',
            'type': 'primary',
            'submitForm': True,
            'icon': 'save',
            'label': _('v_card_scheme_form_save')
          }
        ]
      }
    ]
  }
}
