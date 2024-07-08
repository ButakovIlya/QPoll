import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { FormContainer, FormGridWrapper, StyledForm } from './styled';

import { checkResetPasswordCode, resetPasswordRequest, sendResetPasswordCode } from '@/api/api';
import PassResetHead from '@/components/05_Features/UIComponents/Utils/passResetHead';
import PassResetBtns from '@/components/07_Shared/UIComponents/Buttons/passResetBtns';
import LabeledInput from '@/components/07_Shared/UIComponents/Fields/authLabeledInput';
import { maskTemplates } from '@/config/mask.templates';
import useAuth from '@/hooks/useAuth';
import usePageTitle from '@/hooks/usePageTitle';

const FrmResetPass = () => {
  usePageTitle('restore');
  const [isEmailSubmitted, setIsEmailSubmitted] = useState(false);
  const [isCodeSubmitted, setIsCodeSubmitted] = useState(false);
  const [resetAccountEmail, setResetAccountEmail] = useState('');
  const [resetAccountPasswordToken, setResetAccountPasswordToken] = useState('');
  const [resetAccountCode, setResetAccountCode] = useState();
  const [resetAccountNewPassword, setResetAccountNewPassword] = useState('');
  const navigate = useNavigate();
  const { setAuth } = useAuth();

  const handleEmailSubmit = (event) => {
    event.preventDefault();
    setIsEmailSubmitted(true);
    sendResetPasswordCode({ email: resetAccountEmail });
  };

  const handleCodeSubmit = async (event) => {
    event.preventDefault();
    const checkCodeResponse = await checkResetPasswordCode({
      email: resetAccountEmail,
      reset_code: resetAccountCode,
    });
    if (checkCodeResponse.ok) {
      setIsCodeSubmitted(true);
      setResetAccountPasswordToken(checkCodeResponse.data.reset_token || '');
    }
  };

  const handlePasswordReset = async (event) => {
    event.preventDefault();
    const successReset = await resetPasswordRequest({
      email: resetAccountEmail,
      new_password: resetAccountNewPassword,
      reset_token: resetAccountPasswordToken,
    });
    if (successReset.ok) {
      setAuth(successReset.data.access_token || '');
      navigate('/app');
    }
  };

  const handleSubmit = () => {
    if (isEmailSubmitted) {
      if (isCodeSubmitted) {
        return handlePasswordReset;
      } else {
        return handleCodeSubmit;
      }
    } else {
      return handleEmailSubmit;
    }
  };

  return (
    <FormGridWrapper item>
      <FormContainer>
        <PassResetHead />
        <StyledForm onSubmit={handleSubmit()}>
          {!isEmailSubmitted && (
            <LabeledInput
              label="Введите вашу почту"
              required={true}
              id="email"
              autoComplete="email"
              placeholder="example@mail.ru"
              value={resetAccountEmail}
              handleChange={(e) => setResetAccountEmail(e.target.value)}
            />
          )}
          {isEmailSubmitted && !isCodeSubmitted && (
            <LabeledInput
              label="Введите код восстановления"
              required={true}
              id="code"
              autoComplete="one-time-code"
              placeholder="000-000"
              mask={maskTemplates.restore_code}
              value={resetAccountCode}
              handleChange={(e) => setResetAccountCode(e.target.value)}
            />
          )}
          {isCodeSubmitted && (
            <LabeledInput
              label="Новый пароль"
              required={true}
              id="new-password"
              autoComplete="new-password"
              placeholder="Пароль"
              value={resetAccountNewPassword}
              handleChange={(e) => setResetAccountNewPassword(e.target.value)}
            />
          )}

          <PassResetBtns
            confirmCaption="Отправить"
            returnCaption="Вернуться назад"
            isConfirmDisabled={false}
            returnClick={() => navigate('/signin')}
          />
        </StyledForm>
      </FormContainer>
    </FormGridWrapper>
  );
};

export default FrmResetPass;
