import styled from '@emotion/styled';
import { Box } from '@mui/material';
import { Link } from 'react-router-dom';

import { colorConfig } from '@/app/template/config/color.config';
import { Rem } from '@/utils/convertToRem';

export const StyledAppContentWrapper = styled(Box)(() => ({
  maxWidth: Rem(1200),
  margin: '0 auto',
  padding: `${Rem(100)} 0`,
  width: '100%',
  '@media (max-width: 1300px)': {
    maxWidth: Rem(1000),
  },
  '@media (max-width: 1100px)': {
    maxWidth: Rem(760),
  },
  '@media (max-width: 768px)': {
    padding: 0,
    marginTop: Rem(40),
  },
}));

export const ContentWrapper = styled(Box)({
  display: 'flex',
  flexDirection: 'column',
  rowGap: Rem(20),
  width: '100%',
});

export const PollsGridWrapper = styled(Box)({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  rowGap: Rem(30),
  '@media (max-width: 768px)': {
    padding: Rem(20),
  },
});

export const PollsGrid = styled(Box)({
  display: 'grid',
  gridTemplateColumns: `repeat(auto-fit, minmax(${Rem(400)}, 0.5fr))`,
  gap: '3rem',
  justifyContent: 'start',
  padding: '1rem',
  width: '100%',
  '@media (max-width: 1100px)': {
    gridTemplateColumns: '1fr',
  },
  '@media (max-width: 500px)': {
    gridTemplateColumns: '1fr',
  },
});

export const StyledArchiveLink = styled(Link)({
  alignSelf: 'end',
  display: 'grid',
  gridTemplateColumns: 'auto 1fr',
  alignItems: 'center',
  columnGap: Rem(10),
  color: colorConfig.primaryBlue,
  '@media (max-width: 768px)': {
    fontSize: Rem(14),
    padding: `0 ${Rem(20)}`,
  },
});
