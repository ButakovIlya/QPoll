import styled from '@emotion/styled';
import { Box, Typography } from '@mui/material';

import { Rem } from '@/utils/convertToRem';

export const ConductionBackgroundWrapper = styled(Box)(() => ({
  backgroundColor: '#FAFAFF',
  minHeight: '100vh',
  width: '100%',
}));

export const ConductionWrapper = styled(Box)(() => ({
  display: 'flex',
  alignItems: 'start',
  justifyContent: 'center',
  flexDirection: 'column',
  rowGap: Rem(30),
  maxWidth: Rem(700),
  margin: '0 auto',
  padding: `${Rem(70)} ${Rem(15)}`,
  userSelect: 'none',
  WebkitUserSelect: 'none',
  msUserSelect: 'none',
}));

export const StartBtnWrapper = styled(Box)(() => ({
  width: '100%',
  display: 'flex',
  justifyContent: 'center',
}));

export const VoteEndedText = styled(Typography)(() => ({
  width: '100%',
  textAlign: 'center',
  fontSize: Rem(20),
  fontWeight: 500,
}));
