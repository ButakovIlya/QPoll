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
}));

export const ContentWrapper = styled(Box)({
  display: 'flex',
  flexDirection: 'column',
  rowGap: Rem(20),
  width: '100%',
});

export const PollsGrid = styled(Box)({
  display: 'grid',
  gridTemplateColumns: 'repeat(4, 1fr)',
  gap: Rem(20),
});

export const StyledArchiveLink = styled(Link)({
  alignSelf: 'end',
  display: 'grid',
  gridTemplateColumns: 'auto 1fr',
  alignItems: 'center',
  columnGap: Rem(10),
  color: colorConfig.primaryBlue,
});
