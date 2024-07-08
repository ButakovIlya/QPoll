import styled from '@emotion/styled';
import { Box, Button, Typography } from '@mui/material';

import { Rem } from '@/utils/convertToRem';

export const StyledHeroWrapper = styled(Box)(() => ({
  display: 'grid',
  gridTemplateColumns: '1fr 1fr',
  columnGap: Rem(30),
  alignItems: 'center',
  maxWidth: Rem(1200),
  margin: '0 auto',
  padding: `${Rem(70)} ${Rem(15)}`,
}));

export const StyledLeftColumn = styled(Box)(() => ({
  textAlign: 'left',
}));

export const StyledTypography = styled(Typography)(() => ({
  marginBottom: Rem(45),
  fontSize: Rem(34),
  fontWeight: 700,
  color: '#515151',
}));

export const StyledDescription = styled(Typography)(() => ({}));

export const StyledButton = styled(Button)(() => ({
  backgroundColor: '#007bff',
  color: '#fff',
  padding: `${Rem(10)} ${Rem(20)}`,
  border: 'none',
  cursor: 'pointer',
}));

export const StyledInfoWrapper = styled(Box)(() => ({
  display: 'grid',
  gridTemplateColumns: '1fr 0.75fr',
  columnGap: Rem(15),
  alignItems: 'center',
}));
