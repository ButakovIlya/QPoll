import styled from '@emotion/styled';
import { Box, Drawer, List, Typography } from '@mui/material';
import { Link } from 'react-router-dom';

import { Rem } from '@/utils/convertToRem';

export const StyledDrawer = styled(Drawer)(() => ({
  zIndex: 9000,
  '& .MuiPaper-root': {
    padding: Rem(20),
    maxWidth: Rem(300),
  },
}));

export const BurgerList = styled(List)(() => ({
  display: 'flex',
  flexDirection: 'column',
  rowGap: Rem(15),
}));

export const UserWrapper = styled(Link)(() => ({
  display: 'grid',
  gridTemplateColumns: 'auto 1fr auto',
  alignItems: 'center',
  columnGap: Rem(20),
  marginBottom: Rem(20),
}));

export const UserInfo = styled(Box)(() => ({
  display: 'flex',
  flexDirection: 'column',
}));

export const UserEmail = styled(Typography)(() => ({
  color: '#000',
}));

export const UserRole = styled(Typography)(() => ({
  color: '#000',
}));

export const LinkWrapper = styled(Link)(() => ({
  display: 'flex',
  alignItems: 'center',
  columnGap: Rem(20),
  color: '#000',
}));
