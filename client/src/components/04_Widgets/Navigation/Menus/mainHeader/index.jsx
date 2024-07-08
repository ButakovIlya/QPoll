import { Box, useMediaQuery } from '@mui/material';
import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

import { StyledContainer, StyledHeader, StyledLogoLink } from './styled';

import HeaderNavOut from '@/components/05_Features/DataDisplay/Out/headerNavOut';
import PrimaryButton from '@/components/07_Shared/UIComponents/Buttons/primaryBtn';
import useAuth from '@/hooks/useAuth';

const Header = ({ isMainPage = true }) => {
  const { t } = useTranslation();
  const [isSticky, setIsSticky] = useState(false);
  const { isAuthenticated } = useAuth();

  const isMobile = useMediaQuery('(max-width:768px)');

  useEffect(() => {
    const handleScroll = () => {
      const scrollTop = window.scrollY;
      setIsSticky(scrollTop > 0);
    };

    window.addEventListener('scroll', handleScroll);

    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  return (
    <StyledHeader isSticky={isSticky} isMainPage={isMainPage}>
      <StyledContainer>
        <StyledLogoLink to="/">QPoll</StyledLogoLink>
        <HeaderNavOut isMobile={isMobile}>
          <Box sx={{ display: 'flex', alignItems: 'center', columnGap: '12px' }}>
            <PrimaryButton caption={t('button.createQuiz')} to="/signup" />
            <PrimaryButton
              caption={isAuthenticated ? t('button.profile') : t('button.login')}
              to={isAuthenticated ? '/app' : '/signin'}
            />
          </Box>
        </HeaderNavOut>
      </StyledContainer>
    </StyledHeader>
  );
};

export default Header;
