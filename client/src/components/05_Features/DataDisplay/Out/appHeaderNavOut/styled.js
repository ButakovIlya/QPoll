import styled from '@emotion/styled';
import { NavLink } from 'react-router-dom';

import { colorConfig } from '@/app/template/config/color.config';
import { Rem } from '@/utils/convertToRem';

export const StyledNavigation = styled('nav')(() => ({
  '@media (max-width: 900px)': {
    display: 'none',
  },
}));

export const StyledNavigationList = styled('ul')(() => ({
  display: 'flex',
  alignItems: 'center',
  columnGap: Rem(15),
  '& a:not(:last-child)': {
    paddingRight: Rem(15),
    borderRight: `${Rem(2)} solid #D4D4D4`,
  },
}));

export const StyledNavLink = styled(NavLink)(() => ({
  color: '#909090',
  '&.active': {
    color: colorConfig.primaryBlue,
  },
}));
