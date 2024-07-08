import styled from '@emotion/styled';
import { Box, Grid } from '@mui/material';

import { Rem } from '@/utils/convertToRem';

export const PollListGridContainer = styled(Box)(() => ({
  display: 'grid',
  gridTemplateColumns: 'repeat(2, 1fr)',
  columnGap: Rem(50),
  rowGap: Rem(25),
  width: '100%',
  '@media (max-width: 1000px)': {
    gridTemplateColumns: '1fr',
    gap: Rem(20),
    height: 'auto',
  },
}));

export const CardsWrapper = styled(Grid)(() => ({
  maxHeight: Rem(280),
  '@media (max-width: 1000px)': {
    maxHeight: 'unset',
  },
}));
