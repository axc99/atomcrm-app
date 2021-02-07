var _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; };

const { React, moment, com } = window.globalEnv;
const { view, app } = window.localEnv;
const { useState, useEffect, useMemo } = React;

const { content, strs } = view.data;

const TokenModal = ({ opened, closeTokenModal }) => {
  const [token, setToken] = useState(null);
  const [reqLoading, setReqLoading] = useState(false);

  const getToken = () => {
    setReqLoading(true);
    app.sendReq('getToken', {}).then(result => {
      setReqLoading(false);

      if (result.res == 'ok') {
        setToken(result.token);
      }
    });
  };

  return {
    _com: 'Modal',
    opened,
    onCancel: () => closeTokenModal(),
    title: strs['tokenModal_title'],
    subtitle: strs['tokenModal_subtitle'],
    content: [{
      _com: 'Button',
      _vis: !token,
      type: 'primary',
      label: strs['tokenModal_createToken'],
      onClick: () => getToken(),
      loading: reqLoading
    }, {
      _com: 'Field.Input',
      _vis: !!token,
      value: token,
      label: strs['tokenModal_token'],
      multiline: true,
      type: 'text',
      readOnly: true
    }]
  };
};

view.render = () => {
  const [tokenModal, setTokenModal] = useState({
    opened: false
  });

  const closeTokenModal = () => {
    setTokenModal(_extends({}, tokenModal, {
      opened: false
    }));
  };

  view.methods.openToken = () => {
    setTokenModal(_extends({}, tokenModal, {
      opened: true
    }));
  };

  return {
    header: view.header,
    scheme: [{
      _com: 'Information',
      content
    }, TokenModal(_extends({}, tokenModal, {
      closeTokenModal
    }))]
  };
};