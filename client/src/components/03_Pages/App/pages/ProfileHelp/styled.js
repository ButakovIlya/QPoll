import styled from '@emotion/styled';
import { Avatar, Box, Typography } from '@mui/material';

import { Rem } from '@/utils/convertToRem';

export const StyledProfileAvatar = styled(Avatar)(() => ({
  width: 90,
  height: 90,
  marginTop: Rem(24),
  '&:hover': {
    opacity: 0.7,
    cursor: 'pointer',
  },
}));

export const ProfileTitle = styled(Typography)(() => ({
  fontSize: Rem(24),
}));

export const BoxCaption = styled(Typography)(() => ({
  marginTop: Rem(48),
  fontSize: Rem(18),
  lineHeight: Rem(24),
}));

export const ProfileFieldsWrapper = styled(Box)(() => ({
  display: 'grid',
  gridTemplateColumns: '1fr',
  rowGap: Rem(15),
}));
