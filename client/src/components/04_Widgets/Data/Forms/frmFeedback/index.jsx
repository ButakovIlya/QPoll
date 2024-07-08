import SendIcon from '@mui/icons-material/Send';
import { Box, Button, MenuItem, TextField } from '@mui/material';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';

import { sendTicketFx } from './model/send-ticket';

import { useAlert } from '@/hooks/useAlert';

const FrmFeedback = () => {
  const { t } = useTranslation();
  const { showAlert } = useAlert();
  const [message, setMessage] = useState('');
  const [type, setType] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!type || message.length < 10) {
      showAlert(
        'Пожалуйста, заполните все обязательные поля и убедитесь, что сообщение содержит минимум 10 символов.',
        'info',
      );
      return;
    }

    await sendTicketFx({ type, message });

    showAlert('Обращение успешно отправлено !', 'success');
    setType('');
    setMessage('');
  };

  return (
    <Box component="form" noValidate autoComplete="off" onSubmit={handleSubmit}>
      <TextField
        select
        label="Тип обращения"
        value={type}
        onChange={(e) => setType(e.target.value)}
        required
        fullWidth
        margin="normal"
      >
        <MenuItem value="Жалоба">Жалоба</MenuItem>
        <MenuItem value="Обращение">Предложение</MenuItem>
        <MenuItem value="Вопрос">Вопрос</MenuItem>
      </TextField>
      <TextField
        label="Сообщение"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        required
        fullWidth
        margin="normal"
        multiline
        rows={4}
        inputProps={{ minLength: 10 }}
      />
      <Button type="submit" variant="contained" startIcon={<SendIcon />} sx={{ mt: 2 }}>
        {t('button.send')}
      </Button>
    </Box>
  );
};

export default FrmFeedback;
