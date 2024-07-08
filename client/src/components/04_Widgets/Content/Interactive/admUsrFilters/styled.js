import styled from '@emotion/styled';
import { Box } from '@mui/material';

import { Rem } from '@/utils/convertToRem';

export const FiltersWrapper = styled(Box)(() => ({
  display: 'flex',
  alignItems: 'center',
  padding: Rem(15),
  marginBottom: Rem(20),
  borderRadius: Rem(16),
  backgroundColor: '#fff',
  width: 'fit-content',
}));
