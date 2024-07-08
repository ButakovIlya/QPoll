import { handleRequest } from '@/api/api';

export const filterPollsRequest = async (field, value, setter) => {
  const queryString = value !== '' ? `?${field}=${value}` : '';
  return handleRequest('get', `/api/my_poll/${queryString}`).then((res) =>
    setter(res.data.results)
  );
};
