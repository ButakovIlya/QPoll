import { Box, Typography } from '@mui/material';
import { useParams } from 'react-router-dom';
import { v4 } from 'uuid';

import usePollSettings from './hooks/usePollSettings';

import CustomSwitch from '@/components/07_Shared/UIComponents/Buttons/switch';
import { StyledFormControlLabel } from '@/constants/styles';
import { pollTuningSettings } from '@/data/fields';
import usePollData from '@/hooks/usePollData';

const PollTuningTab = ({ pollData }) => {
  const { id } = useParams();
  const { pollStatus } = usePollData(id);
  const [localSettings, handleSwitchChange] = usePollSettings(pollData);

  return (
    <Box spacing={2}>
      {pollTuningSettings.map((item) => (
        <Box
          key={v4()}
          sx={{ borderBottom: '1px solid #e2e2e2', paddingBottom: '15px', marginTop: '10px' }}
        >
          <Typography sx={{ marginBottom: '10px' }}>{item.heading}</Typography>
          {item.switchSettings.map((item) => (
            <StyledFormControlLabel
              key={v4()}
              control={
                <CustomSwitch
                  disabled={pollStatus}
                  focusVisibleClassName={item.label}
                  onChange={handleSwitchChange(item.id)}
                  checked={localSettings ? localSettings[item.id] ?? false : false}
                />
              }
              label={item.label}
            />
          ))}
        </Box>
      ))}
    </Box>
  );
};

export default PollTuningTab;
