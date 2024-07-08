import styled from '@emotion/styled';
import { Box, Tabs } from '@mui/material';

import { Rem } from '@/utils/convertToRem';

export const TabsButtonsContainer = styled(Box)(() => ({
  backgroundColor: '#fff',
  boxShadow: `0 ${Rem(2)} ${Rem(4)} rgba(0,0,0,.05), 0 ${Rem(8)} ${Rem(20)} rgba(0,0,0,.1)`,
  borderRadius: Rem(5),
}));

export const StyledTabs = styled(Tabs)(() => ({
  '& .MuiTabs-flexContainer': {
    display: 'grid',
    gridTemplateColumns: 'repeat(2,1fr)',
  },
}));
