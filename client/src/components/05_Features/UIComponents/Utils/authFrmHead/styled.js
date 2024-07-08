import styled from '@emotion/styled';
import { Box } from '@mui/material';
import { Rem } from '@/utils/convertToRem';
import { colorConfig } from '@/app/template/config/color.config';

export const FormHeadingContainer = styled(Box)(() => ({
  width: '100%',
  display: 'grid',
  gridTemplateColumns: 'auto',
  marginBottom: Rem(40),
  '& h5': {
    fontSize: Rem(32),
    fontWeight: 600,
  },
  '& p div': {
    display: 'flex',
    columnGap: Rem(10),
  },
  '& button': {
    border: 0,
    backgroundColor: 'transparent',
    color: colorConfig.primaryBlue,
    cursor: 'pointer',
  },
}));
