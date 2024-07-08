import styled from '@emotion/styled';
import { Typography } from '@mui/material';

import { Rem } from '@/utils/convertToRem';

export const StyledLabel = styled(Typography)(() => ({
  backgroundColor: 'rgba(219, 236, 255, 0.8)',
  display: 'inline',
  padding: Rem(3),
  borderRadius: Rem(6),
  fontSize: Rem(12),
}));
