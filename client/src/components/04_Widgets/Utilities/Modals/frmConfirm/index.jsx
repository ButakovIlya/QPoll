import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import { useTranslation } from 'react-i18next';

const FrmConfirm = ({
  open,
  title = 'Подтверждение',
  message = 'Вы уверены?',
  onConfirm,
  onCancel,
}) => {
  const { t } = useTranslation();
  return (
    <Dialog
      open={open}
      onClose={onCancel}
      aria-labelledby="alert-dialog-title"
      aria-describedby="alert-dialog-description"
    >
      <DialogTitle id="alert-dialog-title">{title}</DialogTitle>
      <DialogContent>
        <DialogContentText id="alert-dialog-description">{message}</DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={onCancel} color="primary">
          {t('button.cancel')}
        </Button>
        <Button onClick={onConfirm} color="primary" autoFocus>
          {t('button.apply')}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default FrmConfirm;
