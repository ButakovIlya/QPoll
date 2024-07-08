import CloseIcon from '@mui/icons-material/Close';
import ExitToAppIcon from '@mui/icons-material/ExitToApp';
import { Box } from '@mui/material';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import { memo } from 'react';
import { v4 } from 'uuid';

import {
  CloseButtonWrapper,
  StyledList,
  StyledNavItem,
  StyledNavItemCaption,
  StyledProfileContentWrapper,
  StyledProfileSidebarHeading,
  StyledProfileWrapper,
} from './styled';

const ProfileSidebar = memo(({ linksData = {}, onClose }) => {
  return (
    <StyledProfileWrapper>
      <CloseButtonWrapper>
        <CloseIcon onClick={() => onClose()} />
      </CloseButtonWrapper>
      <StyledProfileContentWrapper>
        <StyledList component="nav" aria-label="main mailbox folders">
          <ListItem>
            <StyledProfileSidebarHeading primary="Аккаунт" />
          </ListItem>
          {linksData.map((item) => (
            <StyledNavItem
              end
              key={v4()}
              to={item.to}
              className={({ isActive, isPending }) =>
                isPending ? 'pending' : isActive ? 'active' : ''
              }
              onClick={() => onClose()}
            >
              <ListItemIcon sx={{ minWidth: 'unset' }}>
                <item.icon />
              </ListItemIcon>
              <StyledNavItemCaption primary={item.caption} />
            </StyledNavItem>
          ))}
        </StyledList>
        <Box sx={{ marginTop: 'auto' }}>
          <StyledNavItem to="/">
            <ListItemIcon>
              <ExitToAppIcon />
            </ListItemIcon>
            <ListItemText primary="Выход" />
          </StyledNavItem>
        </Box>
      </StyledProfileContentWrapper>
    </StyledProfileWrapper>
  );
});

export default ProfileSidebar;
