import { Box, Typography } from '@mui/material';

import {
  DescriptionTagsWrapper,
  DescriptionWrapper,
  GraphWrapper,
  HeaderWrapper,
  ResultContainer,
} from './styled';

import PollNumbResultOut from '@/components/06_Entities/Out/pollNumResOut';
import CustomGauge from '@/components/07_Shared/DataDisplay/Charts/gauge';
import { pollResTableFlds } from '@/data/fields';
import { formatISODateTime } from '@/utils/js/formatDate';

const PollResHead = ({ res, data }) => {
  return (
    <HeaderWrapper>
      <GraphWrapper>
        <CustomGauge value={res.percentage} />
      </GraphWrapper>
      <DescriptionWrapper>
        <DescriptionTagsWrapper>
          <Typography sx={{ fontSize: '12px', color: '#aaa' }}>{data.poll_type}</Typography>
          <Box>
            <Typography sx={{ fontSize: '12px' }}>
              {formatISODateTime(data.result.voting_date)}
            </Typography>
          </Box>
        </DescriptionTagsWrapper>

        <ResultContainer container>
          <PollNumbResultOut data={pollResTableFlds} res={res} />
        </ResultContainer>
      </DescriptionWrapper>
    </HeaderWrapper>
  );
};

export default PollResHead;
