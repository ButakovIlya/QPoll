import { StyledButtonsWrapper, StyledConfirmButton, StyledReturnButton } from './styled';

const PassResetBtns = ({
  returnCaption = '',
  confirmCaption = '',
  isConfirmDisabled = false,
  returnClick = () => {},
}) => {
  return (
    <StyledButtonsWrapper>
      <StyledReturnButton type="button" fullWidth variant="contained" onClick={() => returnClick()}>
        {returnCaption}
      </StyledReturnButton>
      <StyledConfirmButton disabled={isConfirmDisabled} type="submit" fullWidth variant="contained">
        {confirmCaption}
      </StyledConfirmButton>
    </StyledButtonsWrapper>
  );
};

export default PassResetBtns;
