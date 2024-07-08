import { useParams } from 'react-router-dom';

import { StyledButton, StyledNavLink } from './styled';

const PollSettingsMenuBtn = ({ icon: Icon, label, page, disabled }) => {
  const { id } = useParams();

  const handleClick = (event) => {
    if (disabled) {
      event.preventDefault();
    }
  };

  return (
    <StyledNavLink
      end
      to={`/app/tests/${id}/${page}`}
      className={({ isActive, isPending }) => (isPending ? 'pending' : isActive ? 'active' : '')}
      isDisabled={disabled}
      onClick={handleClick}
    >
      <StyledButton
        startIcon={<Icon />}
        component="div"
        style={{ justifyContent: 'flex-start' }}
        disabled={disabled}
        isDisabled={disabled}
      >
        {label}
      </StyledButton>
    </StyledNavLink>
  );
};

export default PollSettingsMenuBtn;
