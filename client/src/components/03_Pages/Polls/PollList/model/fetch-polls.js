import { handleRequest } from '@/api/api';
import { createEffect } from 'effector';

export const fetchAllPollsFx = createEffect(async ({ currPage, pageSize }) => {
  const response = await handleRequest('get', `/api/poll/?page=${currPage}&page_size=${pageSize}`);
  return response.data;
});
