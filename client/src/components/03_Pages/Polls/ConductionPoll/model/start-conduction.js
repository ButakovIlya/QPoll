import { createEffect } from 'effector';

import { handleRequest } from '@/api/api';

export const startConductionFx = createEffect(async ({ id, data }) => {
  const response = await handleRequest('post', `/api/poll_voting_started/?poll_id=${id}`, {
    auth_data: data,
  });
  return response.data;
});
