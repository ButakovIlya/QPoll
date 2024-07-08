import styled from '@emotion/styled';
import { DragIndicator } from '@mui/icons-material';
import { Box } from '@mui/material';

import { Rem } from '@/utils/convertToRem';

export const QueSettingsWrapper = styled(Box)(() => ({
  display: 'grid',
  gridTemplateColumns: '1fr',
  columnGap: 0,
  rowGap: Rem(15),
  alignItems: 'center',
}));

export const StyledDragIndicator = styled(DragIndicator)(({ isFree, status }) => ({
  cursor: isFree || status ? 'default' : 'grab',
  opacity: isFree ? 0 : 1,
  marginRight: Rem(10),
}));

export const QueBtnWrapper = styled(Box)(() => ({
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
  '@media (max-width: 1000px)': {
    flexDirection: 'column',
    alignItems: 'start',
    rowGap: Rem(10),
  },
}));
