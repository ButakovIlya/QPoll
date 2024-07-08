import styled from '@emotion/styled';
import { Box } from '@mui/material';

import { Rem } from '@/utils/convertToRem';

export const QRCodeWrapper = styled(Box)(() => ({
  display: 'grid',
  justifyContent: 'center',
  rowGap: Rem(20),
  padding: Rem(20),
}));
