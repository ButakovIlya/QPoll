import styled from '@emotion/styled';
import { Box, DialogTitle, Typography } from '@mui/material';

import { colorConfig } from '@/app/template/config/color.config';
import { Rem } from '@/utils/convertToRem';

export const StyledDialogTitle = styled(DialogTitle)(() => ({
  fontSize: Rem(14),
  color: '#6F6F6F',
}));

export const DialogContentWrapper = styled(Box)(() => ({
  display: 'grid',
  gridTemplateColumns: 'repeat(4,1fr)',
  columnGap: Rem(20),
  '@media (max-width: 600px)': {
    gridTemplateColumns: '1fr',
    gap: Rem(10),
  },
}));

export const ButtonContainer = styled(Box)(() => ({
  cursor: 'pointer',
  textAlign: 'center',
  padding: `${Rem(20)} ${Rem(10)}`,
  borderRadius: Rem(7),
  boxShadow: `0 ${Rem(8)} ${Rem(20)} rgba(0, 0, 0, 0.1), 0 ${Rem(2)} ${Rem(4)} rgba(0, 0, 0, 0.05)`,
  transition: 'transform 0.3s ease',
  '&:hover': {
    transform: 'translateY(-8px)',
    '& svg': {
      fill: colorConfig.primaryBlue,
    },
  },
}));

export const ButtonContainerTitle = styled(Typography)(() => ({
  marginTop: Rem(20),
  fontSize: Rem(14),
  color: '#515151',
  lineHeight: Rem(18),
  fontWeight: 600,
}));

export const ButtonContainerDescription = styled(Typography)(() => ({
  marginTop: Rem(5),
  fontSize: Rem(12),
  lineHeight: Rem(14),
}));
