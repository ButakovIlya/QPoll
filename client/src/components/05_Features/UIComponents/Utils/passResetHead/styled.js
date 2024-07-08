import { Rem } from '@/utils/convertToRem';
import styled from '@emotion/styled';
import { Typography } from '@mui/material';

export const StyledTypography = styled(Typography)(() => ({
  fontSize: Rem(32),
  fontWeight: 600,
  marginBottom: Rem(40),
}));
