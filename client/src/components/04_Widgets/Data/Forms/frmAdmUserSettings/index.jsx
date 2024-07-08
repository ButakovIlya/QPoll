import {
  Box,
  Button,
  FormControl,
  InputLabel,
  MenuItem,
  Modal,
  Select,
  Typography,
} from '@mui/material';
import { useState } from 'react';

import { changeRoleFx } from './models/change-role';

const styles = {
  modal: {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 400,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
  },
  formControl: {
    marginTop: 2,
    marginBottom: 2,
    minWidth: 120,
  },
  button: {
    marginTop: 2,
  },
};

const FrmAdmUserSettings = ({ open, handleClose, userId, setUsers }) => {
  const [role, setRole] = useState('');

  const handleChange = (event) => setRole(event.target.value);

  const handleSubmit = async (event) => {
    event.preventDefault();
    const response = await changeRoleFx({ userId, role });
    if (response.ok) {
      setUsers((prevUsers) =>
        prevUsers.map((user) => (user.user.id === userId ? { ...user, role: role } : user)),
      );
      handleClose();
    }
  };

  return (
    <Modal open={open} onClose={() => handleClose(false)}>
      <Box sx={styles.modal}>
        <Typography variant="h6" component="h2">
          Настройки пользователя
        </Typography>
        <form onSubmit={handleSubmit}>
          <FormControl fullWidth sx={styles.formControl}>
            <InputLabel id="role-label">Роль</InputLabel>
            <Select
              labelId="role-label"
              id="role-select"
              value={role}
              label="Role"
              onChange={handleChange}
            >
              <MenuItem value="Администратор">Администратор</MenuItem>
              <MenuItem value="Пользователь">Пользователь</MenuItem>
              <MenuItem value="Преподаватель">Преподаватель</MenuItem>
            </Select>
          </FormControl>
          <Button type="submit" variant="contained" color="primary" sx={styles.button}>
            Сохранить
          </Button>
        </form>
      </Box>
    </Modal>
  );
};

export default FrmAdmUserSettings;
