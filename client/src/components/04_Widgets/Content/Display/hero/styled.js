import styled from '@emotion/styled';
import { Box } from '@mui/material';

import { colorConfig } from '@/app/template/config/color.config';
import { Rem } from '@/utils/convertToRem';

const heroBaseStyles = {
  display: 'grid',
  height: '100vh',
  maxWidth: Rem(1200),
  margin: '0 auto',
  padding: `0 ${Rem(15)}`,
  alignItems: 'center',
  justifyContent: 'center',
  textAlign: 'left',
};

export const StyledHeroContainer = styled(Box)(() => ({
  backgroundColor: 'rgba(172, 220, 255, 0.2)',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  padding: `0 ${Rem(15)}`,
}));

export const StyledHero = styled(Box)(({ theme }) => ({
  ...heroBaseStyles,
  gridTemplateColumns: '1fr',
  paddingTop: Rem(60),
  [theme.breakpoints.up('sm')]: {
    paddingTop: Rem(120),
  },
  [theme.breakpoints.up('md')]: {
    ...heroBaseStyles,
    gridTemplateColumns: '1fr 1fr',
  },
  '@media (max-width: 899px)': {
    paddingTop: Rem(80),
  },
}));

export const StyledHeroTextWrapper = styled(Box)(({ theme }) => ({
  justifySelf: 'center',
  maxWidth: Rem(650),
  textAlign: 'center',
  [theme.breakpoints.up('md')]: {
    justifySelf: 'start',
    maxWidth: Rem(550),
    textAlign: 'left',
  },
}));

export const StyledHeroTextHeading = styled('h2')(({ theme }) => ({
  fontSize: Rem(36),
  lineHeight: Rem(45),
  marginBottom: Rem(15),
  [theme.breakpoints.up('sm')]: {
    fontSize: Rem(52),
    lineHeight: Rem(52),
    marginBottom: Rem(20),
  },
  [theme.breakpoints.up('md')]: {
    fontSize: Rem(60),
    lineHeight: Rem(60),
    marginBottom: Rem(25),
  },
}));

export const StyledHeroTextSubHeading = styled('p')(() => ({
  fontSize: Rem(18),
  lineHeight: Rem(30),
  marginBottom: Rem(25),
  color: colorConfig.primaryBlack,
  opacity: '.7',
}));

export const StyledHeroImage = styled('img')(() => ({
  maxWidth: '100%',
  height: 'auto',
  justifySelf: 'end',
  '@media (max-width: 899px)': {
    maxWidth: '80%',
    justifySelf: 'center',
  },
  '@media (max-width: 650px)': {
    maxWidth: '100%',
  },
}));
