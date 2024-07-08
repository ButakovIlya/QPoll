import { StyledButton, StyledDescription, StyledTypography } from './styled';

import {
  StyledFirstHeroWrapper,
  StyledFirstInfoWrapper,
  StyledFirstLeftColumn,
} from '@/constants/styles';

const NoDataHelper = ({
  title = '',
  description,
  btnCaption = '',
  handler = () => {},
  image = '',
}) => {
  return (
    <StyledFirstHeroWrapper>
      <StyledFirstLeftColumn>
        <StyledTypography variant={'h4'}>{title}</StyledTypography>
        <StyledFirstInfoWrapper>
          {description && <StyledDescription variant={'body1'}>{description}</StyledDescription>}
          {btnCaption && <StyledButton onClick={() => handler(true)}>{btnCaption}</StyledButton>}
        </StyledFirstInfoWrapper>
      </StyledFirstLeftColumn>
      <img src={image} alt={`${image}`} />
    </StyledFirstHeroWrapper>
  );
};

export default NoDataHelper;
