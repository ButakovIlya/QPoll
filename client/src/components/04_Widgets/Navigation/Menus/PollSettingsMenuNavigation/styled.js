import styled from '@emotion/styled';
import { Box, Tabs } from '@mui/material';

import { Rem } from '@/utils/convertToRem';

export const StyledNavContainer = styled(Box)(() => ({
  maxWidth: Rem(1200),
  margin: '0 auto',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  padding: `${Rem(20)} ${Rem(15)}`,
  '@media (max-width: 999px)': {
    padding: 0,
  },
}));

export const MobMenuWrapper = styled(Box)(() => ({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  width: '100%',
}));

export const TabsMenu = styled(Tabs)(() => ({
  width: '100%',
  height: '100%',
  '& .MuiTabs-flexContainer': {
    flexDirection: 'column',
    alignItems: 'center',
  },
}));
