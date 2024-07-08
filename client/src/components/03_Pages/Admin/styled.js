import styled from '@emotion/styled';
import { Box, Drawer } from '@mui/material';

import { Rem } from '@/utils/convertToRem';

export const AdminPanelWrapper = styled(Box)(() => ({
  display: 'flex',
  flexDirection: 'column',
  height: '100vh',
}));

export const AdmContentWrapper = styled(Box)(() => ({
  display: 'flex',
  flexGrow: 1,
}));

export const AdmRouterWrapper = styled(Box)(() => ({
  flexGrow: 1,
  backgroundColor: '#F5F6FA',
}));

export const StyledDrawerWrapper = styled(Drawer)(() => ({
  width: Rem(240),
  flexShrink: 0,
  '& .MuiDrawer-paper': {
    width: Rem(240),
    boxSizing: 'border-box',
  },
}));
