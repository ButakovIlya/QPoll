import styled from '@emotion/styled';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import { Dialog, DialogTitle } from '@mui/material';

import { Rem } from '@/utils/convertToRem';

export const ShareDialog = styled(Dialog)(() => ({
  '& .MuiPaper-root': { borderRadius: Rem(24) },
}));

export const ShareDialogTitle = styled(DialogTitle)(() => ({
  backgroundColor: '#e6f6e0',
  display: 'flex',
  alignItems: 'center',
}));

export const StyledCheckIcon = styled(CheckCircleIcon)(() => ({
  width: '1.5em',
  height: '1.5em',
  marginRight: Rem(15),
  color: 'rgb(107, 193, 74)',
}));
