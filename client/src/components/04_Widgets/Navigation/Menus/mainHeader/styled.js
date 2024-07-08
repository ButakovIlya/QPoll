import styled from '@emotion/styled';
import { Box } from '@mui/material';
import { Link } from 'react-router-dom';

import { colorConfig } from '@/app/template/config/color.config';
import { Rem } from '@/utils/convertToRem';

export const StyledHeader = styled('header')(({ isSticky, isMainPage }) => ({
  padding: `${Rem(20)}`,
  position: isMainPage ? 'fixed' : 'relative',
  top: 0,
  left: 0,
  width: '100%',
  background: isSticky ? 'rgba(255, 255, 255, 0.9)' : 'transparent',
  backdropFilter: isSticky ? `blur(${Rem(5)})` : 'none',
  transition: 'background-color 0.3s ease-in-out, backdrop-filter 0.3s ease-in-out',
  boxSizing: 'border-box',
  zIndex: 100,
}));

export const StyledLogoLink = styled(Link)(() => ({
  fontSize: Rem(36),
  color: colorConfig.primaryBlue,
  cursor: 'pointer',
}));

export const StyledContainer = styled(Box)(() => ({
  maxWidth: Rem(1200),
  margin: '0 auto',
  padding: `0 ${Rem(15)}`,
  display: 'grid',
  gridTemplateColumns: '1fr auto',
  alignItems: 'center',
}));
