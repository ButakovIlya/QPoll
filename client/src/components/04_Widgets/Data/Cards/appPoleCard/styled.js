import styled from '@emotion/styled';
import { Box, Card, CardContent, CardMedia, Chip, Typography } from '@mui/material';

import { colorConfig } from '@/app/template/config/color.config';
import { Rem } from '@/utils/convertToRem';

export const StldChip = styled(Chip)(() => ({
  color: 'white',
  backgroundColor: colorConfig.primaryBlue,
  height: Rem(22),
  '& .MuiChip-label': {
    fontSize: Rem(12),
  },
}));

export const StldCard = styled(Card)(() => ({
  borderRadius: Rem(16),
  boxShadow: 'none',
  display: 'grid',
  gridTemplateColumns: '1fr 1fr', // Equal division for two columns
  border: `${Rem(1)} solid ${colorConfig.primaryGray}`,
  position: 'relative',
  overflow: 'hidden',
  transition: 'transform 0.3s ease',
  minHeight: Rem(280), // Set a minimum height to avoid compression
  width: '100%', // Card width is flexible within grid column

  '&:hover': {
    transform: 'translateY(-8px)',
  },

  '@media (max-width: 768px)': {
    flexDirection: 'column',
    gridTemplateColumns: '1fr',
  },
}));

export const StldCardMedia = styled(CardMedia)(() => ({
  backgroundSize: 'cover',
  padding: Rem(25),
  borderRadius: Rem(16),
  '@media (max-width: 768px)': {
    height: Rem(150),
  },
}));

export const StldCardContent = styled(CardContent)(() => ({
  display: 'flex',
  flexDirection: 'column',
  maxHeight: Rem(200),
  overflow: 'hidden',
  alignItems: 'start',
}));

export const ActionsWrapper = styled(Box)(() => ({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  marginBottom: Rem(20),
  width: '100%',
}));

export const ChipsWrapper = styled(Box)(() => ({
  display: 'flex',
  alignItems: 'center',
  width: '100%',
  columnGap: Rem(5),
}));

export const StldPollName = styled(Typography)(() => ({
  color: '#aaa',
  fontSize: Rem(12),
  marginBottom: Rem(10),
}));

export const StldDesc = styled(Box)(() => ({
  maxWidth: '100%',
  overflow: 'hidden',
  textOverflow: 'ellipsis',
  whiteSpace: 'no-wrap',
  WebkitLineClamp: 3,
  display: 'box',
  WebkitBoxOrient: 'vertical',
}));
