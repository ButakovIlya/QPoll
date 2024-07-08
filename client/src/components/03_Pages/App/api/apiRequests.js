import { handleRequest } from '@/api/api';

export const getAllPoles = async ({ currPage, pageSize }) => {
  const data = await handleRequest('get', `/api/my_poll/?page=${currPage}&page_size=${pageSize}`);
  return data.data;
};

export const getProfileData = async () => {
  return handleRequest('get', '/api/my_profile/');
};
