import styled from '@emotion/styled';
import { TableContainer, TableHead } from '@mui/material';
import { Rem } from '@/utils/convertToRem';

export const StyledTableContainer = styled(TableContainer)(() => ({
  borderRadius: Rem(14),
  boxShadow: 'none',
  border: `${Rem(1)} solid #D5D5D5`,
}));

export const StyledTableHead = styled(TableHead)(() => ({
  maxHeight: Rem(50),
  '& th': {
    lineHeight: Rem(16),
    fontWeight: 600,
  },
}));
