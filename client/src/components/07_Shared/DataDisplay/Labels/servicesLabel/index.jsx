import { StyledLabel } from './styled';

const ServicesLabel = ({ caption = '' }) => {
  return <StyledLabel variant="body2">{caption}</StyledLabel>;
};

export default ServicesLabel;
