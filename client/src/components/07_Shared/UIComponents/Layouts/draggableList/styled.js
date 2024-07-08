import styled from '@emotion/styled';
import { Box } from '@mui/material';

import { Rem } from '@/utils/convertToRem';

export const DragWrapper = styled(Box)(({ pollType }) => ({
  display: 'grid',
  gridTemplateColumns:
    pollType === 'Опрос' || pollType === 'Быстрый' ? 'auto 1fr auto' : 'auto auto 1fr auto',
  marginBottom: Rem(10),
  alignItems: 'center',
  '& .MuiBox-root': {
    margin: 0,
  },
}));
