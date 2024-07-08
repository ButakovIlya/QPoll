import { CircularProgress } from '@mui/material';

import { LoaderWrapper } from './styled';

const CLoader = () => {
  return (
    <LoaderWrapper>
      <CircularProgress color="secondary" />
    </LoaderWrapper>
  );
};

export default CLoader;
