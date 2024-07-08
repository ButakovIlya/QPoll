import styled from '@emotion/styled';
import { AppBar, Box, Stack, Toolbar } from '@mui/material';
import { Rem } from '@/utils/convertToRem';

export const StyledAppBar = styled(AppBar)(() => ({
  position: 'static',
  backgroundColor: '#fff',
  boxShadow: 'none',
}));

export const StyledToolbar = styled(Toolbar)(() => ({
  justifyContent: 'space-between',
}));

export const SearchWrapper = styled(Box)(() => ({
  display: 'flex',
  alignItems: 'center',
  borderRadius: Rem(19),
  border: `${Rem(1)} solid #D5D5D5`,
  backgroundColor: '#F5F6FA',
  maxHeight: Rem(35),
  width: Rem(320),
  fontSize: Rem(12),
  '& .MuiInputBase-root': {
    width: '100%',
  },
  '& input::placeholder': {
    fontSize: Rem(13),
  },
}));

export const StyledStack = styled(Stack)(() => ({
  color: '#000',
}));
