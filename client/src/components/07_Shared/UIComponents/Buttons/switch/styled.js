import styled from '@emotion/styled';
import { Switch } from '@mui/material';

import { colorConfig } from '@/app/template/config/color.config';
import { Rem } from '@/utils/convertToRem';

export const IOSSwitch = styled(Switch)(() => ({
  width: 42,
  height: 26,
  padding: 0,
  '& .MuiSwitch-switchBase': {
    padding: 0,
    margin: 2,
    transitionDuration: '300ms',
    '&.Mui-checked': {
      transform: `translateX(${Rem(16)})`,
      color: '#fff',
      '& + .MuiSwitch-track': {
        backgroundColor: colorConfig.primaryBlue,
        opacity: 1,
        border: 0,
      },
      '&.Mui-disabled + .MuiSwitch-track': {
        opacity: 0.5,
      },
    },
    '&.Mui-focusVisible .MuiSwitch-thumb': {
      color: '#33cf4d',
      border: `${Rem(6)} solid #fff`,
    },
    '&.Mui-disabled .MuiSwitch-thumb': {
      color: 'grey',
    },
    '&.Mui-disabled + .MuiSwitch-track': {
      opacity: 0.3,
    },
  },
  '& .MuiSwitch-thumb': {
    boxSizing: 'border-box',
    width: 22,
    height: 22,
  },
  '& .MuiSwitch-track': {
    borderRadius: 26 / 2,
    backgroundColor: '#c6c6c6',
    opacity: 1,
    transition: 'all .5s ease',
  },
}));
