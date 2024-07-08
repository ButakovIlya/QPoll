import { Link } from 'react-router-dom';

import { StyledButton } from './styled';

const SecondaryButton = ({ caption = '', handleClick = () => {}, to, ...linkProps }) => {
  const buttonElement = to ? (
    <Link to={to} {...linkProps}>
      <StyledButton onClick={handleClick}>{caption}</StyledButton>
    </Link>
  ) : (
    <StyledButton onClick={handleClick}>{caption}</StyledButton>
  );

  return buttonElement;
};

export default SecondaryButton;
