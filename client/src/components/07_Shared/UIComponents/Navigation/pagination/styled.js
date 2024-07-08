import styled from '@emotion/styled';
import { Box, Pagination, Stack } from '@mui/material';
import { Rem } from '@utils/convertToRem';

import { colorConfig } from '@/app/template/config/color.config';

export const StyledStack = styled(Stack)(() => ({
  display: 'flex',
  flexDirection: 'row',
  alignItems: 'center',
  columnGap: Rem(20),
  marginTop: Rem(15),
}));

export const StyledPageSizeWrapper = styled(Box)(() => ({
  display: 'flex',
  alignItems: 'center',
  columnGap: Rem(10),
  '& span': {
    fontSize: Rem(14),
    color: '#eee',
    fontWeight: 500,
  },
  '& .MuiInputBase-root': {
    margin: 0,
    borderRadius: Rem(15),
    '& svg': {
      color: '#000',
    },
  },
  '& .MuiSelect-select': {
    padding: Rem(5),
    fontSize: Rem(14),
    fontWeight: 500,
    color: '#000',
  },
}));

export const StyledPagination = styled(Pagination)(() => ({
  borderRadius: Rem(43),
  fontSize: Rem(14),
  fontWeight: 'medium',
  '& .MuiPaginationItem-root.MuiPaginationItem-sizeMedium': {
    padding: '0',
    margin: '0',
    border: '0',
  },
  '& .MuiPaginationItem-outlined.MuiPaginationItem-rounded.Mui-selected': {
    backgroundColor: colorConfig.primaryBlue,
    color: '#fff',
    boxShadow: `0 0 ${Rem(7)} -1px ${colorConfig.primaryBlue}`,
  },
}));
