import styled from '@emotion/styled';
import { Box } from '@mui/material';

import { Rem } from '@/utils/convertToRem';

export const NameWrapper = styled(Box)(({ isLower }) => ({
  display: 'grid',
  gridTemplateColumns: '1fr 1fr',
  padding: `${Rem(8)} 0`,
  borderBottom: isLower ? `${Rem(1)} solid #e0e0e0` : 'none',
}));
