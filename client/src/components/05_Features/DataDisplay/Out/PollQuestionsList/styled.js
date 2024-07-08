import styled from '@emotion/styled';
import { Box, Button, Card, CardContent, Typography } from '@mui/material';

import { colorConfig } from '@/app/template/config/color.config';
import { Rem } from '@/utils/convertToRem';

export const ListWrapper = styled(Box)(() => ({
  width: '100%',
}));

export const StyledAddButton = styled(Button)(() => ({
  marginBottom: Rem(20),
  width: '100%',
  padding: Rem(10),
  borderColor: colorConfig.primaryBlue,
  color: colorConfig.primaryBlue,
  '@media (max-width: 999px)': {
    marginTop: Rem(15),
  },
}));

export const StyledQueCount = styled(Typography)(() => ({
  fontSize: Rem(14),
  color: '#aaa',
  marginBottom: Rem(10),
}));

export const StyledCard = styled(Card)(({ selected }) => ({
  marginBottom: Rem(5),
  boxShadow: selected ? 'none' : 3,
  border: selected ? `${Rem(1)} solid blue` : 'none',
  cursor: 'pointer',
  '& .MuiCardContent-root': {
    paddingBottom: Rem(10),
  },
}));

export const StyledCardContent = styled(CardContent)(() => ({
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
  padding: Rem(10),
}));

export const StyledContentWrapper = styled(Box)(() => ({
  display: 'flex',
  alignItems: 'center',
  columnGap: Rem(10),
  flexGrow: 1,
  '& .MuiTypography-root': {
    color: '#aaa',
    fontSize: Rem(15),
    lineHeight: 1,
  },
}));

export const IconsWrapper = styled(Box)(() => ({
  display: 'flex',
  alignItems: 'center',
  columnGap: Rem(5),
  '& svg': {
    fill: '#aaa',
    width: Rem(22),
    height: Rem(22),
  },
}));

export const QueAccordion = styled(Box)(() => ({
  display: 'grid',
  gridTemplateColumns: '1fr auto',
  alignItems: 'center',
  columnGap: Rem(20),
  width: '100%',
  marginRight: Rem(20),
}));
