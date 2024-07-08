import { Box, Typography } from '@mui/material';

import {
  DescriptionTagsWrapper,
  DescriptionWrapper,
  HeaderWrapper,
  ImageWrapper,
  StyledDescText,
  StyledImage,
  StyledTitle,
} from './styled';

import { formatDateTime } from '@/utils/js/formatDate';

const ConductionHeader = ({ data }) => {
  return (
    <HeaderWrapper>
      <ImageWrapper>
        <StyledImage src={data.image} />
      </ImageWrapper>
      <DescriptionWrapper>
        <DescriptionTagsWrapper>
          <Typography sx={{ fontSize: '12px', color: '#aaa' }}>{data.poll_type?.name}</Typography>
          <Box>
            <Typography sx={{ fontSize: '12px' }}>
              {formatDateTime(data?.poll_setts?.start_time)} -{' '}
              {formatDateTime(data?.poll_setts?.end_time)}
            </Typography>
          </Box>
        </DescriptionTagsWrapper>
        <StyledTitle>{data.name ?? ''}</StyledTitle>
        <StyledDescText>{data.description}</StyledDescText>
      </DescriptionWrapper>
    </HeaderWrapper>
  );
};

export default ConductionHeader;
