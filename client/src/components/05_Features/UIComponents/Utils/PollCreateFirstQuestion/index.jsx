import QuestionsImage from '@assets/QuestionsCreate.svg';
import { Typography } from '@mui/material';

import {
  StyledFirstButton,
  StyledFirstHeroWrapper,
  StyledFirstInfoWrapper,
  StyledFirstLeftColumn,
} from '@/constants/styles';

const PollCreateFirstQuestion = ({ settings = {}, handleCreateQuestion = () => {} }) => {
  return (
    <StyledFirstHeroWrapper>
      <StyledFirstLeftColumn>
        <Typography variant={'h4'} sx={{ marginBottom: '40px' }}>
          {settings.title}
        </Typography>
        <StyledFirstInfoWrapper>
          <StyledFirstButton onClick={() => handleCreateQuestion()}>
            {settings.buttonCaption}
          </StyledFirstButton>
        </StyledFirstInfoWrapper>
      </StyledFirstLeftColumn>
      <img src={QuestionsImage} alt="Описание изображения" />
    </StyledFirstHeroWrapper>
  );
};

export default PollCreateFirstQuestion;
