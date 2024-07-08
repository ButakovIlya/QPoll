import styled from '@emotion/styled';
import { Box, Button, FormGroup } from '@mui/material';

import { Rem } from '@/utils/convertToRem';

export const FiltersWrapper = styled(Box)(() => ({
  width: '95%',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  border: `${Rem(1)} solid black`,
  borderRadius: Rem(10),
  backgroundColor: '#fff',
  marginBottom: Rem(20),
  padding: Rem(10),
  '@media (max-width: 1000px)': {
    display: 'block',
    position: 'sticky',
    top: Rem(20),
    zIndex: 1000,
    padding: 0,
    width: '100%',
  },
}));

export const StyledFormGroup = styled(FormGroup)(() => ({
  width: '100%',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  '@media (max-width: 1000px)': {
    '& button': {
      marginBottom: Rem(10),
    },
  },
}));

export const FiltersButton = styled(Button)(() => ({
  width: '100%',
  justifyContent: 'center',
  py: 2,
}));
