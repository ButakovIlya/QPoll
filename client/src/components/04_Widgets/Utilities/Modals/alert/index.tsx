import { Alert, Snackbar } from '@mui/material';

import { useAlert } from '@/hooks/useAlert';

const AlertPopup = () => {
  const { alert, closeAlert } = useAlert();

  return (
    <Snackbar
      open={alert.open}
      autoHideDuration={3000}
      onClose={closeAlert}
      anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
    >
      <Alert onClose={closeAlert} severity={alert.severity} sx={{ width: '100%' }}>
        {alert.message}
      </Alert>
    </Snackbar>
  );
};

export default AlertPopup;
