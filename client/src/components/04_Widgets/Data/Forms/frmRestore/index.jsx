import { OverlayWrapper, StyledAuthWrapper } from '@/components/03_Pages/Auth/styled';
import FrmResetPass from '@/components/04_Widgets/Data/Forms/frmResetPass';
import AuthIllustration from '@/components/05_Features/UIComponents/Utils/authIllustration';
import React from 'react';

const FrmRestore = () => {
  return (
    <StyledAuthWrapper component="main">
      <OverlayWrapper container>
        <AuthIllustration />
        <FrmResetPass />
      </OverlayWrapper>
    </StyledAuthWrapper>
  );
};

export default FrmRestore;
