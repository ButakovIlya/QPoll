import { createEffect } from 'effector';

import { handleRequest } from '@/api/api';

export const getPollResultsFx = createEffect(async ({ id }) => {
  const data = await handleRequest('get', `/api/my_poll_stats/?poll_id=${id}`);
  return data.data;
});

export const getPollAnswersFx = createEffect(async ({ id }) => {
  const data = await handleRequest('get', `/api/my_poll_users_votes/?poll_id=${id}`);
  return data.data.results;
});
