import styled from '@emotion/styled';
import { Select } from '@mui/material';

export const TypeSelect = styled(Select)(() => ({
  '& .MuiSelect-select': {
    display: 'flex',
    alignItems: 'center',
  },
}));
