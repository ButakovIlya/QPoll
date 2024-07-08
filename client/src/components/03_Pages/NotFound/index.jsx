import ErrorImage from '@assets/404.svg';
import { Container } from '@mui/material';

import { InfoText, TitleText, WorksWrapper } from '@/app/template/base/styles';
import Header from '@/components/04_Widgets/Navigation/Menus/mainHeader';

const NotFoundPage = () => {
  return (
    <Container>
      <Header isMainPage={false} />
      <WorksWrapper>
        <img src={ErrorImage} style={{ maxWidth: '500px' }} />
        <TitleText>Такой страницы нет</TitleText>
        <InfoText>Но есть много других интересных страниц</InfoText>
      </WorksWrapper>
    </Container>
  );
};

export default NotFoundPage;
