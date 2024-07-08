import styled from '@emotion/styled';
import { Box, Typography } from '@mui/material';

import { Rem } from '@/utils/convertToRem';

export const Styled2AuthContainerHeading = styled(Typography)(() => ({
  marginTop: Rem(48),
  fontSize: Rem(18),
  lineHeight: Rem(24),
  '@media (max-width: 768px)': {
    marginTop: Rem(20),
  },
}));

export const StyledAuthContentWrapper = styled(Box)(() => ({
  display: 'grid',
  gridTemplateColumns: 'auto 1fr auto',
  alignItems: 'center',
}));

export const StyledImage = styled('img')(() => ({
  width: Rem(70),
  height: Rem(70),
  marginRight: Rem(15),
}));

export const Styled2AuthHeading = styled(Typography)(() => ({
  fontSize: Rem(14),
  fontWeight: 400,
  color: '#35383a',
  marginBottom: Rem(5),
}));

export const Styled2AuthInfo = styled(Typography)(() => ({
  fontSize: Rem(11),
  fontWeight: 400,
  color: '#697074',
  lineHeight: Rem(14),
}));

export const Stld2AuthInfoWrapper = styled(Box)(() => ({
  marginRight: Rem(100),
  '@media (max-width: 768px)': {
    marginRight: Rem(50),
  },
  '@media (max-width: 450px)': {
    marginRight: Rem(20),
  },
}));
