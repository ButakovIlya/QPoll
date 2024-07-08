import { Typography } from '@mui/material';
import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useLocation, useParams } from 'react-router-dom';

import { CompTimeWrapper } from './styled';

import {
  changePoleData,
  getInfoAboutPole,
} from '@/components/03_Pages/App/pages/Pole/PoleMainSettings/api/apiRequests';
import InvisibleLabeledField from '@/components/07_Shared/UIComponents/Fields/invisibleLabeledField';
import { useAlert } from '@/hooks/useAlert';

const PollDesignSettingsTab = () => {
  const { id } = useParams();
  const { t } = useTranslation();
  const { showAlert } = useAlert();
  const [poleData, setPoleData] = useState();
  const [pendingChanges, setPendingChanges] = useState({});
  const [timeoutHandlers, setTimeoutHandlers] = useState({});

  const location = useLocation();
  const isNewPole = location.state?.isNewPole;

  const fetchPoleData = async () => {
    const responseData = await getInfoAboutPole(id);
    setPoleData(responseData.data);
  };

  useEffect(() => {
    if (!isNewPole) {
      fetchPoleData();
    }
  }, [isNewPole]);

  const handleChange = (fieldName, value) => {
    setPendingChanges((prevState) => ({
      ...prevState,
      [fieldName]: value,
    }));

    if (timeoutHandlers[fieldName]) {
      clearTimeout(timeoutHandlers[fieldName]);
    }

    const handler = setTimeout(async () => {
      await changePoleData(fieldName, value, id, fetchPoleData, showAlert);
      setPendingChanges((prevState) => ({
        ...prevState,
        [fieldName]: undefined,
      }));
    }, 1500);

    setTimeoutHandlers((prevState) => ({
      ...prevState,
      [fieldName]: handler,
    }));
  };

  return (
    <InvisibleLabeledField
      label={
        <CompTimeWrapper>
          {t('label.completionTime')}
          <Typography
            sx={{ textDecoration: 'underline', fontSize: '14px', cursor: 'pointer' }}
            onClick={() => handleChange('completion_time', '00:00')}
          >
            Очистить
          </Typography>
        </CompTimeWrapper>
      }
      type="time"
      min="00:00:00"
      max="23:59:59"
      handleChange={(e) => handleChange('completion_time', e)}
      value={
        pendingChanges['completion_time'] !== undefined
          ? pendingChanges['completion_time']
          : (poleData?.poll_setts?.completion_time !== null &&
              poleData?.poll_setts?.completion_time) ||
            '00:00:00'
      }
    />
  );
};

export default PollDesignSettingsTab;
