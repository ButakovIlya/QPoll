import { Dialog, DialogContent } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { v4 } from 'uuid';

import { createPole } from './api/apiRequests';
import {
  ButtonContainer,
  ButtonContainerDescription,
  ButtonContainerTitle,
  DialogContentWrapper,
  StyledDialogTitle,
} from './styled';

const FrmCreatePoll = ({ isOpen, onClose, title, buttons }) => {
  const navigate = useNavigate();

  const handlePoleTypeSelect = async (poleType) => {
    const newPoleId = v4();
    await createPole(poleType, newPoleId);
    navigate(`/app/tests/${newPoleId}/main`, { state: { isNewPole: true } });
  };

  return (
    <Dialog
      open={isOpen}
      onClose={() => onClose(false)}
      sx={{ '& .MuiPaper-root': { maxWidth: '800px' } }}
    >
      <StyledDialogTitle>{title}</StyledDialogTitle>
      <DialogContent>
        <DialogContentWrapper>
          {buttons.map((button) => (
            <ButtonContainer key={v4()} onClick={() => handlePoleTypeSelect(button.type)}>
              <button.image sx={{ width: '38px', height: '38px' }} />
              <ButtonContainerTitle>{button.title}</ButtonContainerTitle>
              <ButtonContainerDescription>{button.caption}</ButtonContainerDescription>
            </ButtonContainer>
          ))}
        </DialogContentWrapper>
      </DialogContent>
    </Dialog>
  );
};

export default FrmCreatePoll;
