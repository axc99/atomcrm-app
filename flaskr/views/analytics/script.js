const { React, moment } = window.globalEnv
const { view, app } = window.localEnv
const { useState, useEffect, useMemo } = React

view.render = () => {
  // Handle period type change
  view.methods.onChangePeriodType = ({ value }) => {
    app
      .getPage()
      .to({
          periodType: value
      })
  }

  // Handle period change
  view.methods.onChangePeriod = ({ value }) => {
    app
      .getPage()
      .to({
          periodType: view.data['periodType'],
          periodFrom: value[0],
          periodTo: value[1]
      })
  }

  return {
    header: view.header,
    scheme: view.scheme
  }
}
