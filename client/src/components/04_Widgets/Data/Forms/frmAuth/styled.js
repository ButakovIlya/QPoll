import styled from '@emotion/styled';
import { Button, Grid } from '@mui/material';

import { colorConfig } from '@/app/template/config/color.config';
import { Rem } from '@/utils/convertToRem';

export const FormGridWrapper = styled(Grid)(() => ({
  flexBasis: '30%',
  maxWidth: '100%',
  '@media (max-width: 1200px)': {
    flexBasis: '50%',
  },
  '@media (max-width: 900px)': {
    flexBasis: '75%',
  },
  '@media (max-width: 600px)': {
    flexBasis: '100%',
  },
}));

export const FormContainer = styled(Grid)(() => ({
  padding: `0 ${Rem(50)}`,
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
}));

export const StyledForm = styled('form')(() => ({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'start',
  width: '100%',
  '& .MuiTypography-root': {
    margin: 0,
  },
  '& .MuiFormControl-root': {
    margin: `0 0 ${Rem(8)} 0`,
  },
  '& .MuiInputBase-root': {
    borderRadius: Rem(12),
    fontSize: Rem(16),
  },
  '& .MuiInputBase-root input': {
    padding: Rem(12),
  },
  '& .css-md26zr-MuiInputBase-root-MuiOutlinedInput-root.Mui-focused .MuiOutlinedInput-notchedOutline':
    {
      border: `${Rem(2)} solid ${colorConfig.primaryBlue}`,
    },
}));

export const StyledConfirmButton = styled(Button)(({ disabled }) => ({
  marginTop: Rem(30),
  height: Rem(48),
  borderRadius: Rem(30),
  backgroundColor: colorConfig.primaryBlue,
  opacity: disabled ? '0.7' : '1',
  color: '#fff',
}));
