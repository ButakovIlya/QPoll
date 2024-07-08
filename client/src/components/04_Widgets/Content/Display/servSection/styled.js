import styled from '@emotion/styled';
import { Box, Typography } from '@mui/material';

import { Rem } from '@/utils/convertToRem';

export const StyledSection = styled('section')(() => ({
  maxWidth: Rem(1200),
  margin: '0 auto',
  padding: `${Rem(80)} ${Rem(15)}`,
}));

export const StyledSectionHeading = styled(Typography)(() => ({
  marginBottom: Rem(30),
}));

export const StyledCardsWrapper = styled(Box)(() => ({
  display: 'grid',
  gridTemplateColumns: `repeat(auto-fill, minmax(${Rem(300)}, 1fr))`,
  gap: Rem(20),
  justifyContent: 'space-around',
  '@media (max-width: 650px)': {
    gridTemplateColumns: `repeat(auto-fill, minmax(${Rem(280)}, 1fr))`,
    gap: Rem(10),
  },
}));
