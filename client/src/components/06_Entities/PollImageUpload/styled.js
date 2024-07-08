import styled from '@emotion/styled';
import { Button } from '@mui/material';

import { Rem } from '@/utils/convertToRem';

export const StyledImageButton = styled(Button)(() => ({
  border: `${Rem(1)} dashed #C9C9C9`,
  minHeight: Rem(200),
  lineHeight: Rem(145),
  cursor: 'pointer',
  columnGap: Rem(15),
  backgroundColor: '#F7F7F7',
  marginBottom: Rem(20),
}));

export const InvisibleInput = styled('input')({
  display: 'none',
});
