import styled from '@emotion/styled';
import { Box, Typography } from '@mui/material';
import Input from '@mui/material/Input';

import { Rem } from '@/utils/convertToRem';

export const LabeledFieldWrapper = styled(Box)(() => ({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'start',
  marginTop: Rem(10),
}));

export const StyledLabelTypography = styled(Typography)(() => ({
  fontSize: Rem(14),
  width: '100%',
  color: '#6f6f6f',
}));

export const StyledInput = styled(Input)(() => ({
  '&::before, &::after': { content: 'none' },
}));
