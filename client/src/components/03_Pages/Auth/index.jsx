import { useCallback, useEffect, useMemo, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

import { OverlayWrapper, StyledAuthWrapper } from './styled';

import { loginUser, registerUser } from '@/api/api';
import FrmAuth from '@/components/04_Widgets/Data/Forms/frmAuth';
import AuthIllustration from '@/components/05_Features/UIComponents/Utils/authIllustration';
import { useAlert } from '@/hooks/useAlert';
import useAuth from '@/hooks/useAuth';
import usePageTitle from '@/hooks/usePageTitle';

const AuthPage = () => {
  const { setAuth } = useAuth();
  const navigate = useNavigate();
  const { showAlert } = useAlert();
  const location = useLocation();
  const path = useMemo(() => location.pathname, [location.pathname]);
  const [isSignIn, setIsSignIn] = useState(path === '/signin');
  usePageTitle(isSignIn ? 'login' : 'signup');

  useEffect(() => {
    const storedToken = localStorage.getItem('auth_token');
    if (storedToken) navigate('/app');
  }, [navigate]);

  const handleFormSwitch = useCallback(() => {
    setIsSignIn((prev) => !prev);
    navigate(isSignIn ? '/signup' : '/signin');
  }, [isSignIn, navigate]);

  const handleFormSubmit = useCallback(
    async (event) => {
      const formData = {
        email: event.email,
        password: event.password,
        ...(isSignIn
          ? {}
          : {
              number: event.number,
              name: event.name,
              surname: event.surname,
              patronymic: event.patronymic,
            }),
      };

      try {
        const response = isSignIn ? await loginUser(formData) : await registerUser(formData);
        if (response.data.access_token && response.data.access_token.length > 0) {
          localStorage.setItem('refresh_token', response.data.refresh_token);
          setAuth(response.data.access_token);
          showAlert('Вход успешно выполнен !', 'success');
          setTimeout(() => {
            navigate('/app');
          }, 1300);
        }
      } catch (error) {
        showAlert('Логин или пароль неверные !', 'error');
      }
    },
    [isSignIn],
  );

  return (
    <StyledAuthWrapper component="main">
      <OverlayWrapper container>
        <AuthIllustration />
        <FrmAuth
          isSignIn={isSignIn}
          handleFormSwitch={handleFormSwitch}
          handleFormSubmit={handleFormSubmit}
        />
      </OverlayWrapper>
    </StyledAuthWrapper>
  );
};

export default AuthPage;
