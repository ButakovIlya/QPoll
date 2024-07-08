import { createEffect } from 'effector';

import { handleRequest } from '@/api/api';

export const fetchPollQuestions = createEffect(async (id) => {
  const data = await handleRequest('get', `/api/poll/?poll_id=${id}`);
  return data.data;
});
