import { createContext, useMemo, useState } from 'react';

const AlertContext = createContext();

export const AlertProvider = ({ children }) => {
  const [alert, setAlert] = useState({
    open: false,
    message: '',
    severity: 'info',
  });

  const showAlert = (message, severity = 'info') => {
    setAlert({ open: true, message, severity });
  };

  const closeAlert = () => {
    setAlert({ ...alert, open: false });
  };

  const value = useMemo(() => ({ alert, showAlert, closeAlert }), [alert, showAlert, closeAlert]);

  return <AlertContext.Provider value={value}>{children}</AlertContext.Provider>;
};

export default AlertContext;
