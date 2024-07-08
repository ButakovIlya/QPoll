import axios from 'axios';

import { handleRequest } from '@/api/api';
import config from '@/config';

const timeouts = {};

export const getInfoAboutPole = async (id) => {
  return handleRequest('get', `/api/my_poll/?poll_id=${id}&detailed=0`);
};

export const changePoleData = async (field, value, id, setPoleData, showAlert, fetchPoleData) => {
  if (timeouts[field]) {
    clearTimeout(timeouts[field]);
  }

  if ((field === 'start_time' || field === 'end_time') && value === '') {
    value = null;
  }

  const requestData = { [field]: value };

  setPoleData((prevData) => ({
    ...prevData,
    [field]: value,
  }));

  if (field === 'image') {
    axios.patch(`${config.serverUrl.main}/api/my_poll/?poll_id=${id}`, requestData, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('auth_token') ?? ''}`,
        'content-type': 'multipart/form-data',
      },
    });
  }

  timeouts[field] = setTimeout(() => {
    handleRequest(
      'patch',
      `/api/my_poll${field === 'start_time' || field === 'end_time' || field === 'duration' ? '_settings' : ''}/?poll_id=${id}`,
      requestData,
    ).then((res) => {
      if (res.response && res.response.status !== 200) {
        showAlert(res.response.data.message.error, 'error');
        fetchPoleData();
      } else {
        fetchPoleData();
        showAlert('Данные об опросе успешно сохранены !', 'success');
      }
    });
    delete timeouts[field];
  }, 0);
};
