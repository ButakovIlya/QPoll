import CloseIcon from '@mui/icons-material/Close';
import { DialogContent } from '@mui/material';
import { useState } from 'react';

import { ShareDialog, ShareDialogTitle, StyledCheckIcon } from './styled';

import FrmShareMain from '@/components/05_Features/Data/Forms/frmShareMain';
import FrmShareQR from '@/components/05_Features/Data/Forms/frmShareQR';

const FrmShare = ({ open, setOpen, caption = '' }) => {
  const [activeView, setActiveView] = useState('main');

  const handleSwitchView = (view) => setActiveView(view);

  return (
    <ShareDialog
      open={open}
      onClose={() => {
        setOpen(false);
        setActiveView('main');
      }}
    >
      <ShareDialogTitle>
        <StyledCheckIcon color="success" />
        {caption}
        <CloseIcon
          onClick={() => {
            setOpen(false);
            setActiveView('main');
          }}
          sx={{ marginLeft: 'auto', cursor: 'pointer' }}
        />
      </ShareDialogTitle>
      <DialogContent sx={{ p: '0' }}>
        {activeView === 'main' && <FrmShareMain setView={handleSwitchView} />}
        {activeView === 'qr' && <FrmShareQR setView={handleSwitchView} />}
      </DialogContent>
    </ShareDialog>
  );
};

export default FrmShare;
