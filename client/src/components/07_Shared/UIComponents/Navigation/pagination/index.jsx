import { pageSizesSettings } from '@config/pagination.config';
import { MenuItem, Select } from '@mui/material';
import { memo } from 'react';

import { StyledPageSizeWrapper, StyledPagination, StyledStack } from './styled';

const CustomPagination = memo(
  ({ caption = '', pageSize, totalPages, currentPage, handlePageSizeChange, handlePageChange }) => {
    return (
      <StyledStack>
        <StyledPageSizeWrapper>
          <span>{caption}</span>
          <Select value={pageSize} onChange={(e) => handlePageSizeChange(Number(e.target.value))}>
            {pageSizesSettings.map((size) => (
              <MenuItem key={size} value={size}>
                {size}
              </MenuItem>
            ))}
          </Select>
        </StyledPageSizeWrapper>
        <StyledPagination
          count={totalPages}
          page={currentPage}
          onChange={(_, page) => handlePageChange(page)}
          variant="outlined"
          shape="rounded"
        />
      </StyledStack>
    );
  },
);

export default CustomPagination;
