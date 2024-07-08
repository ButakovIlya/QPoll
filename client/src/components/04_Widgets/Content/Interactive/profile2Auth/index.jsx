import SecurityIcon from '@assets/security.svg';
import { FormControlLabel } from '@mui/material';
import { useState } from 'react';

import { connect2AuthFx } from './model/connect-2auth';
import {
  Stld2AuthInfoWrapper,
  Styled2AuthContainerHeading,
  Styled2AuthHeading,
  Styled2AuthInfo,
  StyledAuthContentWrapper,
  StyledImage,
} from './styled';

import CustomSwitch from '@/components/07_Shared/UIComponents/Buttons/switch';
import { StyledProfileContainer, StyledProfileFieldsBox } from '@/constants/styles';

const Profile2AuthBlock = ({ caption = '' }) => {
  const [qrCode, setQrCode] = useState('');

  const handleConnect2Auth = () => {
    connect2AuthFx({ setQrCode });
  };

  return (
    <StyledProfileContainer>
      <Styled2AuthContainerHeading variant="h6">{caption}</Styled2AuthContainerHeading>
      <StyledProfileFieldsBox>
        <StyledAuthContentWrapper>
          <StyledImage src={SecurityIcon} alt="Security icon" />
          <Stld2AuthInfoWrapper>
            <Styled2AuthHeading>Двухфакторная аутентификация</Styled2AuthHeading>
            <Styled2AuthInfo>
              Добавьте дополнительную безопасность своей учетной записи, используя двухфакторную
              аутентификацию
            </Styled2AuthInfo>
          </Stld2AuthInfoWrapper>
          <FormControlLabel
            control={
              <CustomSwitch
                focusVisibleClassName={'.Mui-focusVisible'}
                onChange={() => handleConnect2Auth()}
              />
            }
          />
        </StyledAuthContentWrapper>
        {qrCode ? (
          <img src={`data:image/jpeg;base64,${qrCode}`} alt="QR Code" />
        ) : (
          <p>Загрузка QR-кода...</p>
        )}
      </StyledProfileFieldsBox>
    </StyledProfileContainer>
  );
};
export default Profile2AuthBlock;
