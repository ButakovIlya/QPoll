import FilterListIcon from '@mui/icons-material/FilterList';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import { Box, Button, Divider, IconButton, Menu, MenuItem } from '@mui/material';
import React, { useState } from 'react';
import { v4 } from 'uuid';

import { FiltersWrapper } from './styled';

import { admUsrsFilterCategories } from '@/data/filters';

const AdmUsrFilters = () => {
  const [anchorEl, setAnchorEl] = useState(null);
  const [selectedFilter, setSelectedFilter] = useState({});

  const handleClick = (event, category) => {
    setAnchorEl(event.currentTarget);
    setSelectedFilter(category);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleResetFilters = () => {
    // console.log('Фильтры сброшены');
  };

  return (
    <FiltersWrapper>
      <FilterListIcon />
      {admUsrsFilterCategories.map((category) => (
        <React.Fragment key={v4()}>
          <Divider orientation="vertical" flexItem sx={{ mx: 2 }} />
          <Button onClick={(e) => handleClick(e, category)} sx={{ color: '#000' }}>
            {category.name}
          </Button>
          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl) && selectedFilter.id === category.id}
            onClose={handleClose}
          >
            {category.options.map((option) => (
              <MenuItem key={v4()} onClick={handleClose}>
                {option}
              </MenuItem>
            ))}
          </Menu>
        </React.Fragment>
      ))}
      <Box sx={{ flexGrow: 1 }} />
      <IconButton color="default" onClick={handleResetFilters}>
        <RestartAltIcon />
      </IconButton>
    </FiltersWrapper>
  );
};

export default AdmUsrFilters;
