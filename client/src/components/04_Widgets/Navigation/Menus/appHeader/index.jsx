import { Dropdown } from '@mui/base/Dropdown';
import { Menu } from '@mui/base/Menu';
import { MenuItem } from '@mui/base/MenuItem';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import { Button } from '@mui/material';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';

import {
  Listbox,
  StyledHeaderContainer,
  StyledHeaderLogo,
  StyledHeaderProfile,
  StyledHeaderWrapper,
  StyledMenuIcon,
} from './styled';

import AppHeaderNavOut from '@/components/05_Features/DataDisplay/Out/appHeaderNavOut';
import AppBurgerMenu from '@/components/05_Features/UIComponents/Layouts/appBurger';
import { appHeaderData } from '@/data/navigation';
import useAuth from '@/hooks/useAuth';
import useUserData from '@/hooks/useUserData';
import { useUserRole } from '@/hooks/useUserRole';

const AppHeader = () => {
  const { t } = useTranslation();
  const { role } = useUserRole();
  const { setAuth } = useAuth();
  const navigate = useNavigate();
  const userData = useUserData();
  const [drawerOpen, setDrawerOpen] = useState(false);

  const toggleDrawer = (open) => (event) => {
    if (event.type === 'keydown' && (event.key === 'Tab' || event.key === 'Shift')) {
      return;
    }
    setDrawerOpen(open);
  };

  const handleLogOut = () => {
    setAuth(false);
    navigate('/');
  };

  return (
    <StyledHeaderWrapper>
      <StyledHeaderContainer>
        <StyledHeaderLogo to="/">QPoll</StyledHeaderLogo>
        <AppHeaderNavOut itemsData={appHeaderData} />
        <StyledMenuIcon onClick={toggleDrawer(true)} />
        <AppBurgerMenu
          drawerOpen={drawerOpen}
          toggleDrawer={toggleDrawer}
          userData={userData}
          role={role}
          onExit={handleLogOut}
        />
        <Dropdown>
          <StyledHeaderProfile>
            {userData?.email ?? ''}({role})
            <AccountCircleIcon fontSize="small" />
          </StyledHeaderProfile>
          <Menu slots={{ listbox: Listbox }}>
            {role === 'Администратор' && (
              <MenuItem>
                <Button onClick={() => navigate('/admin-panel')}>
                  {t('navigation.adminPanel')}
                </Button>
              </MenuItem>
            )}
            <MenuItem>
              <Button onClick={() => navigate('/app/profile')}>{t('navigation.profile')}</Button>
            </MenuItem>
            <MenuItem>
              <Button onClick={() => handleLogOut()}>{t('navigation.logOut')}</Button>
            </MenuItem>
          </Menu>
        </Dropdown>
      </StyledHeaderContainer>
    </StyledHeaderWrapper>
  );
};

export default AppHeader;
