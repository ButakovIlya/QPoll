import { useEffect, useState } from 'react';

import { changeUserDataFx } from './models/change-user-data';
import {
  BoxCaption,
  ProfileFieldsWrapper,
  ProfileTitle,
  StyledProfileAvatar,
  StyledProfileContainer,
} from './styled';

import ProfileAccFld from '@/components/07_Shared/UIComponents/Fields/profileAccFld';
import { StyledProfileFieldsBox } from '@/constants/styles';

const ProfileUserData = ({ caption = '', boxCaption = '', ProfileInfoFields = [], user_id }) => {
  const [fieldValues, setFieldValues] = useState({});

  useEffect(() => {
    const initialFieldValues = ProfileInfoFields.reduce((acc, { key, initialValue }) => {
      acc[key] = initialValue;
      return acc;
    }, {});

    setFieldValues(initialFieldValues);
  }, [ProfileInfoFields]);

  const handleFieldChange = async (field, value) => {
    setFieldValues((prevValues) => ({
      ...prevValues,
      [field]: value,
    }));
    changeUserDataFx({ user_id, field, value });
  };

  return (
    <StyledProfileContainer>
      <ProfileTitle variant="h4" gutterBottom>
        {caption}
      </ProfileTitle>
      <StyledProfileAvatar src="/path/to/anonymous-avatar.png" alt="Анонимный профиль" />
      <BoxCaption variant="h6" gutterBottom>
        {boxCaption}
      </BoxCaption>
      <StyledProfileFieldsBox>
        <ProfileFieldsWrapper>
          {ProfileInfoFields?.map(({ label, id, disabled, key }) => (
            <ProfileAccFld
              key={id}
              label={label}
              required={false}
              id={id}
              value={fieldValues[key]}
              fieldKey={key}
              handleChange={handleFieldChange}
              disabled={disabled}
            />
          ))}
        </ProfileFieldsWrapper>
      </StyledProfileFieldsBox>
    </StyledProfileContainer>
  );
};

export default ProfileUserData;
