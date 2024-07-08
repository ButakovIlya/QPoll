import styled from '@emotion/styled';
import { Box } from '@mui/material';

import { Rem } from '@/utils/convertToRem';

export const TabPanelWrapper = styled(Box)(() => ({
  backgroundColor: '#fff',
  marginTop: Rem(10),
  borderRadius: Rem(5),
  boxShadow: `0 ${Rem(2)} ${Rem(4)} rgba(0,0,0,.05), 0 ${Rem(8)} ${Rem(20)} rgba(0,0,0,.1)`,
}));
