import styled from '@emotion/styled';
import { Box, Typography } from '@mui/material';

import { Rem } from '@/utils/convertToRem';

export const WorksWrapper = styled(Box)(() => ({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  height: '80vh',
  textAlign: 'center',
}));

export const TitleText = styled(Typography)(() => ({
  fontSize: Rem(26),
  fontWeight: 500,
}));

export const InfoText = styled(Typography)(() => ({
  fontSize: Rem(18),
  fontWeight: 500,
  color: '#868686',
}));
