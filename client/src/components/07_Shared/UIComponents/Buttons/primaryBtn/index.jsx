import { Link } from 'react-router-dom';

import { StyledButton } from './styled';

const PrimaryButton = ({
  caption = '',
  handleClick = () => {},
  to,
  disabled = false,
  style = {},
  ...linkProps
}) => {
  const buttonElement = to ? (
    <Link to={disabled ? '' : to} {...linkProps}>
      <StyledButton onClick={handleClick} style={style}>
        {caption}
      </StyledButton>
    </Link>
  ) : (
    <StyledButton onClick={handleClick} disabled={disabled} style={style}>
      {caption}
    </StyledButton>
  );

  return buttonElement;
};

export default PrimaryButton;
