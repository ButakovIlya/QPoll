import { Box, Grid, styled } from '@mui/material';

export const StyledAuthWrapper = styled(Box)(() => ({
  width: '100vw',
  height: '100vh',
  maxWidth: '100vw',
  maxHeight: '100vh',
}));

export const OverlayWrapper = styled(Grid)(() => ({
  width: '100vw',
  height: '100vh',
  position: 'relative',
  '@media (max-width: 1200px)': {
    justifyContent: 'center',
  },
}));
