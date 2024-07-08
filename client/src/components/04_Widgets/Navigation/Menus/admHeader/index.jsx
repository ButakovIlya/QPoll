import { Notifications as NotificationsIcon, Search as SearchIcon } from '@mui/icons-material';
import { Avatar, Badge, IconButton, InputBase, Stack, Typography } from '@mui/material';

import { SearchWrapper, StyledAppBar, StyledStack, StyledToolbar } from './styled';

import useTicketsCount from '@/hooks/admin/useTicketsCount';
import useUserData from '@/hooks/useUserData';

const AdmHeader = () => {
  const userData = useUserData();
  const { ticketsCount } = useTicketsCount();

  return (
    <StyledAppBar>
      <StyledToolbar>
        <SearchWrapper>
          <IconButton>
            <SearchIcon />
          </IconButton>
          <InputBase placeholder="Поиск" inputProps={{ 'aria-label': 'search' }} />
        </SearchWrapper>

        <StyledStack direction="row" spacing={2} alignItems="center">
          <IconButton aria-label="show new notifications" color="black">
            <Badge badgeContent={ticketsCount} color="error">
              <NotificationsIcon />
            </Badge>
          </IconButton>
          <Avatar src="/static/images/avatar/1.jpg" />
          <Stack direction="column" spacing={0}>
            <Typography variant="body2" noWrap component="div">
              {userData?.name ?? '[Name]'}
            </Typography>
            <Typography variant="caption" noWrap component="div">
              {userData?.role}
            </Typography>
          </Stack>
        </StyledStack>
      </StyledToolbar>
    </StyledAppBar>
  );
};

export default AdmHeader;
