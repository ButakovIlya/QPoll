import { Box } from '@mui/material';

import { TabPanelWrapper } from './styled';

const CustomTabPanel = ({ children, value, index, ...other }) => {
  return (
    <TabPanelWrapper role="tabpanel" hidden={value !== index} {...other}>
      <Box sx={{ p: 3 }}>{children}</Box>
    </TabPanelWrapper>
  );
};

export default CustomTabPanel;
