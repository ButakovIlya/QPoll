import { Typography } from '@mui/material';
import { Link } from 'react-router-dom';

import { BoxCaption, ProfileFieldsWrapper, ProfileTitle } from './styled';

import FrmFeedback from '@/components/04_Widgets/Data/Forms/frmFeedback';
import { StyledProfileContainer, StyledProfileFieldsBox } from '@/constants/styles';

const ProfileHelpPage = () => {
  return (
    <StyledProfileContainer>
      <ProfileTitle>Помощь</ProfileTitle>
      <BoxCaption variant="h6" gutterBottom>
        База знаний (FAQ)
      </BoxCaption>
      <StyledProfileFieldsBox>
        <ProfileFieldsWrapper>
          <Typography> Ответы на многие вопросы вы найдете в базе знаний QPoll</Typography>
          <Link to="#">Перейти в базу знаний</Link>
        </ProfileFieldsWrapper>
      </StyledProfileFieldsBox>
      <BoxCaption variant="h6" gutterBottom>
        Обратная связь
      </BoxCaption>
      <StyledProfileFieldsBox>
        <ProfileFieldsWrapper>
          <FrmFeedback />
        </ProfileFieldsWrapper>
      </StyledProfileFieldsBox>
    </StyledProfileContainer>
  );
};

export default ProfileHelpPage;
