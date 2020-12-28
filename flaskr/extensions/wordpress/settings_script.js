const { React, moment, com } = window.globalEnv
const { view, app } = window.localEnv
const { useState, useEffect, useMemo } = React

const { useForm } = com.Form
const { strs } = view.data

view.render = () => {
  return {
    header: view.header,
    scheme: [
      'FORM!!1'
    ]
  }
}
