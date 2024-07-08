import React from 'react';
import { Box } from '@mui/material';
import { StyledFooter, StyledFooterWrapper, StyledLogoLink } from './styled';

const Footer = () => {
  return (
    <StyledFooter>
      <StyledFooterWrapper>
        <StyledLogoLink to="/">QPoll</StyledLogoLink>
        <Box>
          <p>Vkontakte</p>
        </Box>
      </StyledFooterWrapper>
    </StyledFooter>
  );
};

export default Footer;
