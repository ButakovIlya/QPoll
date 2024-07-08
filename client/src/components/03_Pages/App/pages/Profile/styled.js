import styled from '@emotion/styled';
import { Box } from '@mui/material';

import { Rem } from '@/utils/convertToRem';

export const SidebarWrapper = styled(Box)(({ isSideOpen }) => ({
  width: Rem(240),
  flexShrink: 0,
  transition: 'transform 0.3s ease',
  '@media (max-width: 1000px)': {
    position: 'fixed',
    height: '100%',
    top: 0,
    left: 0,
    width: Rem(240),
    transform: isSideOpen ? 'translateX(0)' : 'translateX(-100%)',
    zIndex: 1200,
    boxShadow: `${Rem(2)} 0 ${Rem(12)} rgba(0,0,0,0.5)`,
    backgroundColor: '#fff',
  },
}));

export const ProfileWrapper = styled(Box)(() => ({
  display: 'flex',
  width: '100%',
  height: '100vh',
}));

export const ProfileContentWrapper = styled(Box)(() => ({
  flex: 1,
  backgroundColor: '#f7f9fa',
  overflowY: 'auto',
}));

export const MobMenuWrapper = styled(Box)(() => ({
  padding: Rem(16),
  backgroundColor: '#e0e0e0',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
}));
