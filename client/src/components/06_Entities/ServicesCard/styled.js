import styled from '@emotion/styled';
import { Box, Typography } from '@mui/material';

import { Rem } from '@/utils/convertToRem';

export const StyledCard = styled(Box)(() => ({
  borderRadius: Rem(30),
  padding: Rem(30),
  boxShadow: `0 ${Rem(2)} ${Rem(3)} 0 rgba(0,0,0,0.4)`,
  '@media (max-width: 650px)': {
    maxWidth: '100%',
  },
}));

export const StyledCardHeading = styled(Typography)(() => ({
  marginBottom: Rem(10),
}));

export const StyledLabelWrapper = styled(Box)(() => ({
  display: 'flex',
  flexWrap: 'wrap',
  gap: Rem(5),
}));
