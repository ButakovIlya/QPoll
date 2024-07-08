import styled from '@emotion/styled';
import { Typography } from '@mui/material';

import { Rem } from '@/utils/convertToRem';

export const SelectedTimezoneText = styled(Typography)(() => ({
  marginTop: Rem(48),
  fontSize: Rem(18),
  lineHeight: Rem(24),
  '@media (max-width: 768px)': {
    marginTop: Rem(20),
  },
}));
