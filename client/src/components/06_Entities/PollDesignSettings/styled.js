import styled from '@emotion/styled';
import { Box } from '@mui/material';

export const CompTimeWrapper = styled(Box)(() => ({
  display: 'grid',
  gridTemplateColumns: '1fr auto',
  alignItems: 'center',
  width: '100%',
}));
