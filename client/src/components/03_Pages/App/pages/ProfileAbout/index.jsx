import CloseIcon from '@mui/icons-material/Close';
import { Box, IconButton } from '@mui/material';
import { useNavigate } from 'react-router-dom';

import { ProfileInfoFieldsConfig } from './data/ProfileInfoFields';
import { StyledProfileAboutWrapper } from './styled';

import Profile2AuthBlock from '@/components/04_Widgets/Content/Interactive/profile2Auth';
import ProfileTimezone from '@/components/04_Widgets/Content/Interactive/profileTimezone';
import ProfileUserData from '@/components/04_Widgets/Content/Interactive/profileUserData';
import useUserData from '@/hooks/useUserData';

const ProfileAboutPage = () => {
  const userData = useUserData();
  const navigate = useNavigate();

  const profileInfoFields = userData
    ? ProfileInfoFieldsConfig.map((field) => ({
        ...field,
        initialValue: field.keys
          ? field.keys.map((key) => userData[key]).join(' ')
          : userData[field.key],
      }))
    : [];

  console.log(userData);

  return (
    <StyledProfileAboutWrapper>
      <IconButton sx={{ position: 'absolute', right: 8, top: 8 }} onClick={() => navigate('/app')}>
        <CloseIcon />
      </IconButton>
      <Box>
        <ProfileUserData
          caption="Профиль"
          boxCaption="Данные аккаунта"
          ProfileInfoFields={profileInfoFields}
          user_id={userData?.user?.id}
        />
        <ProfileTimezone caption="Язык и страна" selectCaption="Часовой пояс" />
        <Profile2AuthBlock caption="Безопасность" />
      </Box>
    </StyledProfileAboutWrapper>
  );
};

export default ProfileAboutPage;
