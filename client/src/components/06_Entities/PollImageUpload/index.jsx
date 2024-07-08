import DeleteIcon from '@mui/icons-material/Delete';
import PhotoCamera from '@mui/icons-material/PhotoCamera';
import { Box, IconButton } from '@mui/material';
import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

import { InvisibleInput, StyledImageButton } from './styled';

import config from '@/config';

const PollImageUpload = ({ image = '', onFileSelect, handleDelete, disabled }) => {
  const { t } = useTranslation();
  const [preview, setPreview] = useState('');

  useEffect(() => {
    if (image) {
      setPreview(config.serverUrl.main + image);
    }
  }, [image]);

  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
        onFileSelect(file);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleFileClear = () => {
    handleDelete();
    setPreview('');
  };

  return (
    <Box
      sx={{ width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2 }}
    >
      {preview ? (
        <>
          <img src={preview} alt="Preview" style={{ maxWidth: '100%', maxHeight: '200px' }} />
          <IconButton onClick={handleFileClear} color="error">
            <DeleteIcon />
          </IconButton>
        </>
      ) : (
        <StyledImageButton sx={{ width: '100%' }} component="label" disabled={disabled}>
          <PhotoCamera />
          {t('button.selectImage')}
          <InvisibleInput accept="image/*" type="file" hidden onChange={handleFileChange} />
        </StyledImageButton>
      )}
    </Box>
  );
};

export default PollImageUpload;
