import styled from '@emotion/styled';
import { Box, Button, Typography } from '@mui/material';

import { Rem } from '@/utils/convertToRem';

export const CardWrapper = styled(Box)(() => ({
  padding: Rem(20),
  boxShadow: `0 ${Rem(2)} ${Rem(4)} rgba(0,0,0,.05), 0 ${Rem(8)} ${Rem(20)} rgba(0,0,0,.1)`,
  borderRadius: Rem(10),
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  '& .MuiChartsLegend-series': {
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    whiteSpace: 'nowrap',
  },
  '& .MuiPie-chart-root .recharts-text': {
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    whiteSpace: 'nowrap',
  },
}));

export const CardInfoWrapper = styled(Box)(() => ({
  alignSelf: 'flex-start',
  width: '100%',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
}));

export const CardHeading = styled(Typography)(() => ({
  fontSize: Rem(15),
  fontWeight: 600,
}));

export const CardAnswersCount = styled(Typography)(() => ({
  fontSize: Rem(13),
}));

export const InfoButton = styled(Button)(() => ({
  fontSize: Rem(14),
  textTransform: 'none',
  textDecoration: 'underline',
  color: '#aaa',
  '&:hover': {
    backgroundColor: 'transparent',
  },
}));
