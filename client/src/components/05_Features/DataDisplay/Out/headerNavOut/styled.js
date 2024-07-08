import styled from '@emotion/styled';
import { Link } from 'react-router-dom';

import { colorConfig } from '@/app/template/config/color.config';
import { Rem } from '@/utils/convertToRem';

export const StyledNavigation = styled('nav')(() => ({
  display: 'grid',
  gridAutoFlow: 'column',
  columnGap: Rem(30),
  alignItems: 'center',
}));

export const StyledNavigationLink = styled(Link)(() => ({
  color: colorConfig.primaryBlack,
  opacity: '.7',
  display: 'grid',
  alignItems: 'center',
  gridTemplateColumns: 'auto 1fr',
  columnGap: Rem(10),
}));
