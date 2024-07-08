import styled from '@emotion/styled';
import { Box, Typography } from '@mui/material';

import { Rem } from '@/utils/convertToRem';

export const HeaderWrapper = styled(Box)(() => ({
  width: `calc(100% - ${Rem(40)})`,
  border: `${Rem(1)} solid #D7D7D7`,
  padding: Rem(20),
  borderRadius: Rem(16),
  backgroundColor: '#fff',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  columnGap: Rem(20),
}));

export const RegTitle = styled(Typography)(() => ({
  fontWeight: 500,
  fontSize: Rem(18),
}));

export const ContentWrapper = styled(Box)(() => ({
  width: '100%',
}));

export const StartBtnWrapper = styled(Box)(() => ({
  width: '100%',
  display: 'flex',
  justifyContent: 'center',
  marginTop: Rem(20),
}));
