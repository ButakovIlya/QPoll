import AdminPanelSettingsIcon from '@mui/icons-material/AdminPanelSettings';
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';
import { Avatar, Typography } from '@mui/material';
import { v4 } from 'uuid';

import {
  BurgerList,
  LinkWrapper,
  StyledDrawer,
  UserEmail,
  UserInfo,
  UserRole,
  UserWrapper,
} from './styled';

import { appHeaderMobileData } from '@/data/navigation';

const AppBurgerMenu = ({ drawerOpen, toggleDrawer, userData, role, onExit }) => {
  return (
    <StyledDrawer anchor="right" open={drawerOpen} onClose={toggleDrawer(false)}>
      <BurgerList>
        <UserWrapper to={'/app/profile'}>
          <Avatar src="/static/images/avatar/1.jpg" />
          <UserInfo>
            <UserEmail>{userData?.email ?? ''}</UserEmail>
            <UserRole>{role}</UserRole>
          </UserInfo>
          <KeyboardArrowRightIcon />
        </UserWrapper>
        {appHeaderMobileData(onExit).map((item) => (
          <LinkWrapper key={v4()} to={item.to} onClick={item.onClick}>
            <item.icon />
            <Typography>{item.caption}</Typography>
          </LinkWrapper>
        ))}
        {role === 'Администратор' && (
          <LinkWrapper key={v4()} to="/admin-panel">
            <AdminPanelSettingsIcon />
            <Typography>Админ-панель</Typography>
          </LinkWrapper>
        )}
      </BurgerList>
    </StyledDrawer>
  );
};

export default AppBurgerMenu;
