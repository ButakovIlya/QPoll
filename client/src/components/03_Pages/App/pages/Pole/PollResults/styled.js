import styled from '@emotion/styled';
import { Box, Select } from '@mui/material';

import { Rem } from '@/utils/convertToRem';

export const Wrapper = styled(Box)(() => ({
  display: 'flex',
  flexDirection: 'column',
  width: '100%',
  maxWidth: Rem(1200),
  margin: `${Rem(24)} auto`,
  columnGap: Rem(30),
  padding: `0 ${Rem(15)}`,
  '@media (max-width: 1250px)': {
    padding: '0',
  },
}));

export const StldSelect = styled(Select)(() => ({
  display: 'flex',
  alignItems: 'center',
  '& .MuiSelect-select': {
    padding: 0,
  },
  '& .MuiOutlinedInput-notchedOutline': {
    border: 0,
  },
}));

export const SettingsWrapper = styled(Box)(() => ({
  display: 'flex',
  alignItems: 'center',
  columnGap: Rem(15),
  width: '100%',
  marginBottom: Rem(20),
}));

export const ResultsGridWrapper = styled(Box)(() => ({
  display: 'grid',
  gridTemplateColumns: 'repeat(2, 1fr)',
  gap: Rem(30),
  width: '100%',
  '@media (max-width: 1250px)': {
    gridTemplateColumns: '1fr',
  },
}));
