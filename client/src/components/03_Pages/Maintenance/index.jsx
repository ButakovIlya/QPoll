import TechWorks from '@assets/works.svg';
import { Container } from '@mui/material';

import { InfoText, TitleText, WorksWrapper } from '@/app/template/base/styles';
import Header from '@/components/04_Widgets/Navigation/Menus/mainHeader';

const MaintenancePage = () => {
  return (
    <Container>
      <Header isMainPage={false} />
      <WorksWrapper>
        <img src={TechWorks} style={{ maxWidth: '500px' }} />
        <TitleText>Ведутся технические работы</TitleText>
        <InfoText>В течении некоторого времени сервис будет недоступен</InfoText>
      </WorksWrapper>
    </Container>
  );
};

export default MaintenancePage;
