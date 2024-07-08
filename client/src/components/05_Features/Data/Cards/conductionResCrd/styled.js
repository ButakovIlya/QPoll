import { colorConfig } from '@/app/template/config/color.config';
import { Rem } from '@/utils/convertToRem';
import styled from '@emotion/styled';
import { Box, FormControl, Typography } from '@mui/material';

export const StyledFormControl = styled(FormControl)(() => ({
  border: `${Rem(1)} solid #D7D7D7`,
  borderRadius: `${Rem(16)}`,
  padding: Rem(20),
  width: '100%',
  backgroundColor: '#fff',
}));

export const OptionsWrapper = styled(Box)(() => ({
  marginTop: Rem(20),
  display: 'grid',
  rowGap: Rem(10),
}));

export const StyledOption = styled(Box)(({ isCorrect }) => ({
  backgroundColor:
    isCorrect === true
      ? colorConfig.primaryGreen
      : isCorrect === false
      ? colorConfig.primaryRed
      : '#fff',
  borderRadius: Rem(10),
}));

export const OptionName = styled(Typography)(() => ({
  padding: Rem(5),
}));
