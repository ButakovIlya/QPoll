import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';

import { FormContainer, FormGridWrapper, StyledConfirmButton, StyledForm } from './styled';

import AuthFrmHead from '@/components/05_Features/UIComponents/Utils/authFrmHead';
import LabeledInput from '@/components/07_Shared/UIComponents/Fields/authLabeledInput';
import { maskTemplates } from '@/config/mask.templates';
import { pattern } from '@/config/validation.patterns';
import { validateField } from '@/utils/js/validateField';

const FrmAuth = ({ isSignIn, handleFormSwitch = () => {}, handleFormSubmit = () => {} }) => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [formErrors, setFormErrors] = useState({
    email: '',
    password: '',
    name: '',
    surname: '',
    patronymic: '',
  });
  const [formValues, setFormValues] = useState({
    email: '',
    password: '',
    number: '',
    name: '',
    surname: '',
    patronymic: '',
  });

  const handleSubmit = (e) => {
    e.preventDefault();

    const emailError = validateField(
      formValues.email,
      pattern.email,
      'Некорректный адрес электронной почты',
    );
    const passwordError = validateField(
      formValues.password,
      pattern.passwordLowerAndUpper,
      'Пароль должен содержать минимум 8 символов, включая строчные и заглавные буквы',
    );

    const nameError = validateField(
      formValues.name,
      pattern.name,
      'Имя должно содержать только буквы кириллицы',
    );

    const surnameError = validateField(
      formValues.name,
      pattern.name,
      'Фамилия должна содержать только буквы кириллицы',
    );

    const patronymicError = validateField(
      formValues.name,
      pattern.name,
      'Отчество должно содержать только буквы кириллицы',
    );

    setFormErrors({
      email: emailError,
      password: passwordError,
      name: nameError,
      surname: surnameError,
      patronymic: patronymicError,
    });

    if (!emailError && !passwordError) {
      handleFormSubmit(formValues);
    }
  };

  const handleInputChange = (e) => {
    setFormValues((prev) => ({ ...prev, [e.target.id]: e.target.value }));
  };

  return (
    <FormGridWrapper item>
      <FormContainer>
        <AuthFrmHead isSignIn={isSignIn} handleFormSwitch={handleFormSwitch} />
        <StyledForm onSubmit={handleSubmit}>
          <LabeledInput
            label="Ваша почта"
            required={true}
            autoComplete="email"
            id="email"
            placeholder="Эл. почта"
            handleChange={handleInputChange}
            errorMessage={formErrors.email}
          />
          <LabeledInput
            label="Пароль"
            required={true}
            autoComplete="current-password"
            id="password"
            placeholder="Пароль"
            handleChange={handleInputChange}
            errorMessage={formErrors.password}
          >
            {isSignIn ? (
              <button onClick={() => navigate('/password-reset')}>{t('button.forgotPass')}</button>
            ) : (
              ''
            )}
          </LabeledInput>
          {!isSignIn && (
            <>
              <LabeledInput
                label="Фамилия"
                required={true}
                autoComplete="additional-name"
                id="surname"
                handleChange={handleInputChange}
                placeholder="Ваша фамилия"
              />
              <LabeledInput
                label="Имя"
                required={true}
                autoComplete="given-name"
                id="name"
                handleChange={handleInputChange}
                placeholder="Ваше имя"
              />
              <LabeledInput
                label="Отчество"
                required={true}
                autoComplete="family-name"
                id="patronymic"
                handleChange={handleInputChange}
                placeholder="Ваше отчество"
              />
              <LabeledInput
                label="Телефон"
                required={true}
                autoComplete="tel"
                id="number"
                handleChange={handleInputChange}
                placeholder="Телефон"
                mask={maskTemplates.phone}
              />
            </>
          )}
          <StyledConfirmButton disabled={false} type="submit" fullWidth variant="contained">
            {isSignIn ? t('button.login') : t('button.signup')}
          </StyledConfirmButton>
        </StyledForm>
      </FormContainer>
    </FormGridWrapper>
  );
};
export default FrmAuth;
