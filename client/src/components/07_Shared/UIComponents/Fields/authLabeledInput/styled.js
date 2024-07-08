import styled from '@emotion/styled';
import { Box } from '@mui/material';

import { colorConfig } from '@/app/template/config/color.config';

export const StyledPasswordWrapper = styled(Box)(() => ({
  display: 'grid',
  width: '100%',
  alignItems: 'center',
  gridTemplateColumns: '1fr auto',
  '& button': {
    backgroundColor: 'transparent',
    border: 1,
    cursor: 'pointer',
    color: colorConfig.primaryBlue,
  },
}));
