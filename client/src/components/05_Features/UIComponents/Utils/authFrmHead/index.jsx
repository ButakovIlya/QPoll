import { Box, Typography } from '@mui/material';
import { useTranslation } from 'react-i18next';

import { FormHeadingContainer } from './styled';

const AuthFrmHead = ({ isSignIn, handleFormSwitch }) => {
  const { t } = useTranslation();
  return (
    <FormHeadingContainer>
      <Typography variant="h5" gutterBottom>
        {isSignIn ? 'Вход' : 'Регистрация'}
      </Typography>
      <Typography variant="body2" gutterBottom>
        <Box>
          <span>{isSignIn ? 'Нет аккаунта ?' : 'Уже есть аккаунт?'}</span>
          <button onClick={handleFormSwitch}>
            {isSignIn ? t('button.registration') : t('button.login')}
          </button>
        </Box>
      </Typography>
    </FormHeadingContainer>
  );
};

export default AuthFrmHead;
