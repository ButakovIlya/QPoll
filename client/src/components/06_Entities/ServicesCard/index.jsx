import { v4 } from 'uuid';

import { StyledCard, StyledCardHeading, StyledLabelWrapper } from './styled';

import ServicesLabel from '@/components/07_Shared/DataDisplay/Labels/servicesLabel';

const ServicesCard = ({ caption = '', buttons = [] }) => {
  return (
    <StyledCard>
      <img src="#" alt="" />
      <StyledCardHeading variant="h6">{caption}</StyledCardHeading>
      <StyledLabelWrapper>
        {buttons.map((btn) => {
          return <ServicesLabel key={v4()} caption={btn} />;
        })}
      </StyledLabelWrapper>
    </StyledCard>
  );
};

export default ServicesCard;
