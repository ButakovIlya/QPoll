import styled from '@emotion/styled';
import { Grid } from '@mui/material';

import { colorConfig } from '@/app/template/config/color.config';
import { Rem } from '@/utils/convertToRem';

export const IllustrationGridWrapper = styled(Grid)(() => ({
  display: 'flex',
  flexDirection: 'column',
  padding: Rem(60),
  backgroundColor: colorConfig.primaryBlue,
  flexBasis: '69%',
  maxWidth: '70%',
  '& a': {
    fontSize: Rem(36),
    color: '#000',
  },
  '& img': {
    maxWidth: '50%',
    height: '100%',
    alignSelf: 'center',
  },
  '@media (max-width: 1200px)': {
    display: 'none',
  },
}));
