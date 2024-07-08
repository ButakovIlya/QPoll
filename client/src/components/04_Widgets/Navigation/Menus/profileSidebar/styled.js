import styled from '@emotion/styled';
import { Box, List, ListItemText } from '@mui/material';
import { NavLink } from 'react-router-dom';

import { colorConfig } from '@/app/template/config/color.config';
import { Rem } from '@/utils/convertToRem';

export const StyledProfileWrapper = styled(Box)(() => ({
  height: '100vh',
  display: 'flex',
  alignItems: 'end',
  boxShadow: `${Rem(10)} 0 ${Rem(20)} 0 rgba(0,0,0,0.3)`,
  width: Rem(240),
  '@media (max-width: 1000px)': {
    position: 'fixed',
    zIndex: 9000,
    top: 0,
    left: 0,
    height: '100%',
    boxShadow: `0 0 ${Rem(10)} rgba(0, 0, 0, 0.5)`,
  },
}));

export const CloseButtonWrapper = styled(Box)(() => ({
  position: 'absolute',
  top: Rem(10),
  right: Rem(10),
  zIndex: 9001,
  display: 'block',
  '@media (min-width: 1001px)': {
    display: 'none',
  },
}));

export const StyledList = styled(List)(() => ({
  padding: `${Rem(18)} ${Rem(24)} ${Rem(24)}`,
}));

export const StyledProfileContentWrapper = styled(Box)(() => ({
  height: '100%',
  width: '100%',
  display: 'flex',
  flexDirection: 'column',
}));

export const StyledProfileSidebarHeading = styled(ListItemText)(() => ({
  marginBottom: Rem(15),
  '& .MuiTypography-root': {
    fontSize: Rem(24),
    color: '#35383a',
  },
}));

export const StyledNavItem = styled(NavLink)(() => ({
  display: 'grid',
  gridTemplateColumns: 'auto 1fr',
  alignItems: 'center',
  columnGap: Rem(15),
  fontSize: Rem(20),
  width: '100%',
  borderRadius: Rem(8),
  transition: 'all .3s ease',
  padding: `${Rem(5)}`,
  '&:not(:first-of-type)': {
    marginTop: Rem(10),
  },
  '&:hover': {
    backgroundColor: 'rgba(93,101,252,.3)',
  },
  '&.active': {
    '& .MuiTypography-root, .MuiSvgIcon-root': {
      color: colorConfig.primaryBlue,
    },
  },
}));

export const StyledNavItemCaption = styled(ListItemText)(() => ({
  '& .MuiTypography-root': {
    fontSize: Rem(16),
    color: '#000',
  },
}));
