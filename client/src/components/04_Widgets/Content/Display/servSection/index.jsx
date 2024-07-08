import { v4 } from 'uuid';

import ServicesCard from '../../../../06_Entities/ServicesCard';

import { StyledCardsWrapper, StyledSection, StyledSectionHeading } from './styled';

import { servicesCardsData } from '@/data/services';

const ServSection = () => {
  return (
    <StyledSection className="services">
      <StyledSectionHeading variant="h4">Какие задачи решает сервис ?</StyledSectionHeading>
      <StyledCardsWrapper>
        {servicesCardsData.map((item) => {
          return <ServicesCard key={v4()} caption={item.caption} buttons={item.buttons} />;
        })}
      </StyledCardsWrapper>
    </StyledSection>
  );
};

export default ServSection;
