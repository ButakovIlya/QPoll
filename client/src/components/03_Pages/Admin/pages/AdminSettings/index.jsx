import { Box, Grid, Paper, TextField, Typography } from '@mui/material';
import { useEffect, useState } from 'react';
import { v4 } from 'uuid';

import { changeSettingsFx } from './model/change-settings';
import { getSettingsFx } from './model/get-settings';

import { pollAdminSettings } from '@/data/fields';

const AdminSettings = () => {
  const [settingsData, setSettingsData] = useState();

  useEffect(() => {
    const fetchSettings = async () => {
      const data = await getSettingsFx();
      setSettingsData(data);
    };
    fetchSettings();
  }, []);

  const handleChange = async (event, link) => {
    const value = Number(event.target.value);
    const data = await changeSettingsFx({ link, value });
    setSettingsData(data);
  };

  return (
    <Box sx={{ p: 2 }}>
      <Paper sx={{ p: 2, mt: 2 }}>
        <Typography variant="h6" sx={{ mt: 4, mb: 2 }}>
          Настройки опроса
        </Typography>
        {pollAdminSettings.map((item) => (
          <Grid container spacing={2} alignItems="center" key={v4()}>
            <Grid item xs={9}>
              <Typography>{item.caption}</Typography>
            </Grid>
            <Grid item xs={3}>
              <TextField
                type="number"
                fullWidth
                label={item.label}
                variant="standard"
                value={settingsData ? settingsData[item.link] : ''}
                onChange={(e) => handleChange(e, item.link)}
              />
            </Grid>
          </Grid>
        ))}
      </Paper>
    </Box>
  );
};

export default AdminSettings;
