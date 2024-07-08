import zaglushka from '@assets/zaglushka.jpg';
import MoreHorizIcon from '@mui/icons-material/MoreHoriz';
import { Box, Menu, MenuItem, Typography } from '@mui/material';
import React, { useState } from 'react';

import { closePollFx } from './model/close-poll';
import { deletePollFx } from './model/delete-poll';
import { duplicatePollFx } from './model/duplicate-poll';
import {
  ActionsWrapper,
  ChipsWrapper,
  StldCard,
  StldCardContent,
  StldCardMedia,
  StldChip,
  StldDesc,
  StldPollName,
} from './styled';

import config from '@/config';

const AppPoleCard = React.memo(({ pollData, fetchData, cardButton }) => {
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);

  const handleMenuToggle = (event) => {
    event.preventDefault();
    setAnchorEl(event.currentTarget === anchorEl ? null : event.currentTarget);
  };

  const handleAction = async (e, effectFn, id = pollData.poll_id) => {
    e.preventDefault();
    await effectFn(id);
    fetchData();
    setAnchorEl(null);
  };

  return (
    <StldCard>
      <StldCardMedia
        image={pollData.image ? `${config.serverUrl.main}/${pollData.image}` : zaglushka}
        title="Poll Image"
      />
      <StldCardContent>
        <ActionsWrapper>
          <ChipsWrapper>
            {pollData.is_anonymous && <StldChip label="Анонимный" />}
            {cardButton && (
              <StldChip label={pollData.is_in_production ? 'Открыт' : 'Регистрация'} />
            )}
            {!cardButton && (
              <StldChip label={!pollData.is_in_production ? 'Недоступен' : 'Доступен'} />
            )}
          </ChipsWrapper>
          {!cardButton && (
            <Box zIndex="tooltip">
              <MoreHorizIcon onClick={handleMenuToggle} />
              <Menu anchorEl={anchorEl} open={open} onClose={() => setAnchorEl(null)}>
                <MenuItem onClick={(e) => handleAction(e, closePollFx)}>Закрыть опрос</MenuItem>
                <MenuItem onClick={(e) => handleAction(e, duplicatePollFx)}>
                  Копировать опрос
                </MenuItem>
                <MenuItem onClick={(e) => handleAction(e, deletePollFx)}>Удалить опрос</MenuItem>
              </Menu>
            </Box>
          )}
        </ActionsWrapper>
        <StldPollName gutterBottom>{pollData.poll_type.name ?? ''}</StldPollName>
        <Typography sx={{ fontSize: '14px', fontWeight: 600 }}>{pollData.name ?? ''}</Typography>
        <StldDesc>
          <Typography noWrap>{pollData.description ?? ''}</Typography>
        </StldDesc>
        {cardButton}
      </StldCardContent>
    </StldCard>
  );
});

export default AppPoleCard;
