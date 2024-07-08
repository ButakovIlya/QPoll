import { FormControl, MenuItem, Select, Typography } from '@mui/material';
import React, { useEffect } from 'react';
import { v4 } from 'uuid';

import { SelectedTimezoneText } from './styled';

import { StyledProfileContainer, StyledProfileFieldsBox } from '@/constants/styles';
import useFormInput from '@/hooks/useFormInput';

const ProfileTimezone = ({ caption = '', selectCaption = '', options = [] }) => {
  const selectedOption = useFormInput('');

  useEffect(() => {
    const getAllTimeZones = async () => {
      await fetch('http://worldtimeapi.org/api/timezone').then((res) => {
        const data = res;
      });
    };
    getAllTimeZones();
  }, []);

  return (
    <StyledProfileContainer>
      <SelectedTimezoneText variant="h6" gutterBottom>
        {caption}
      </SelectedTimezoneText>
      <StyledProfileFieldsBox>
        <FormControl fullWidth>
          <Typography id="demo-simple-select-label" sx={{ marginBottom: '6px', fontSize: '14px' }}>
            {selectCaption}
          </Typography>
          <Select
            labelId="demo-simple-select-label"
            id="demo-simple-select"
            value={selectedOption.value}
            onChange={selectedOption.onChange}
            sx={{ padding: '6px', '& .MuiSelect-select': { padding: 0 } }}
          >
            {options.map((option) => (
              <MenuItem key={v4()} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </StyledProfileFieldsBox>
    </StyledProfileContainer>
  );
};

export default ProfileTimezone;
