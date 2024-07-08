import styled from '@emotion/styled';
import { Box } from '@mui/material';

import { Rem } from '@/utils/convertToRem';

export const PollListPageContentWrapper = styled(Box)(() => ({
  display: 'grid',
  gridTemplateColumns: '1fr 3fr',
  columnGap: Rem(30),
  alignItems: 'start',
  maxWidth: Rem(1500),
  margin: '0 auto',
  padding: `${Rem(70)} ${Rem(15)}`,
  '@media (max-width: 1000px)': {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'stretch',
    padding: `${Rem(50)} ${Rem(10)}`,
    minHeight: '80vh',
  },
}));

export const ContentWrapper = styled(Box)(() => ({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  rowGap: '30px',
}));
