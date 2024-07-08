import styled from '@emotion/styled';
import { Box, TextField, Typography } from '@mui/material';

import { colorConfig } from '@/app/template/config/color.config';
import { Rem } from '@/utils/convertToRem';

export const StyledTypography = styled(Typography)(() => ({
  marginBottom: Rem(5),
}));

export const StyledTextField = styled(TextField)(() => ({
  margin: 0,
  '& .MuiInputBase-input': {
    margin: 0,
    padding: Rem(12),
  },
}));

export const StyledPasswordWrapper = styled(Box)(() => ({
  display: 'grid',
  width: '100%',
  alignItems: 'center',
  gridTemplateColumns: '1fr auto',

  '& button': {
    backgroundColor: 'transparent',
    border: 0,
    cursor: 'pointer',
    color: colorConfig.primaryBlue,
  },
}));
