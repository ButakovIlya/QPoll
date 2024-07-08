import styled from '@emotion/styled';
import { Box, Button, FormControlLabel, Typography } from '@mui/material';

import { Rem } from '@/utils/convertToRem';

export const StyledProfileContainer = styled(Box)(() => ({
  maxWidth: Rem(580),
  margin: '0 auto',
  padding: `${Rem(50)} ${Rem(20)} 0 ${Rem(20)}`,
  '@media (max-width: 768px)': {
    padding: `${Rem(25)} ${Rem(20)} 0 ${Rem(20)}`,
  },
}));

export const StyledProfileFieldsBox = styled(Box)(() => ({
  marginTop: Rem(12),
  marginBottom: Rem(10),
  padding: Rem(15),
  backgroundColor: '#fff',
  boxShadow: `0 ${Rem(1)} ${Rem(3)} rgba(140,148,155,0.1),0 ${Rem(5)} ${Rem(10)} rgba(140,148,155,0.08)`,
  borderRadius: Rem(10),
}));

export const StyledFormControlLabel = styled(FormControlLabel)(() => ({
  maxWidth: 'max-content',
  '& .MuiTypography-root': {
    fontSize: Rem(14),
    color: '#909090',
  },
}));

// First block (if not created smth yet)

export const StyledFirstHeroWrapper = styled(Box)(() => ({
  display: 'grid',
  gridTemplateColumns: '1fr 1fr',
  columnGap: Rem(30),
  alignItems: 'center',
  maxWidth: Rem(1200),
  margin: '0 auto',
  padding: `${Rem(70)} ${Rem(15)}`,
  '@media (max-width: 900px)': {
    gridTemplateColumns: '1fr',
    textAlign: 'center',
    padding: `${Rem(50)} ${Rem(10)}`,
  },
  '@media (max-width: 600px)': {
    padding: `${Rem(30)} ${Rem(10)}`,
  },
}));

export const StyledFirstLeftColumn = styled(Box)(() => ({
  textAlign: 'left',
  '@media (max-width: 900px)': {
    textAlign: 'center',
    marginBottom: Rem(20),
  },
}));

export const StyledFirstTypography = styled(Typography)(() => ({
  marginBottom: Rem(45),
  fontSize: Rem(34),
  fontWeight: 700,
  color: '#515151',
  '@media (max-width: 900px)': {
    fontSize: Rem(28),
    marginBottom: Rem(30),
  },
  '@media (max-width: 600px)': {
    fontSize: Rem(24),
    marginBottom: Rem(20),
  },
}));

export const StyledFirstButton = styled(Button)(() => ({
  backgroundColor: '#007bff',
  color: '#fff',
  padding: `${Rem(10)} ${Rem(20)}`,
  border: 'none',
  cursor: 'pointer',
  '@media (max-width: 900px)': {
    padding: `${Rem(8)} ${Rem(16)}`,
  },
  '@media (max-width: 600px)': {
    padding: `${Rem(6)} ${Rem(12)}`,
  },
}));

export const StyledFirstInfoWrapper = styled(Box)(() => ({
  display: 'grid',
  gridTemplateColumns: '1fr 0.75fr',
  columnGap: Rem(15),
  alignItems: 'center',
  '@media (max-width: 900px)': {
    gridTemplateColumns: '1fr',
    rowGap: Rem(15),
  },
}));
