import { createEffect } from 'effector';

import { handleRequest } from '@/api/api';

export const regOnPollFx = createEffect(async ({ poll_id }) => {
  const data = await handleRequest('post', `/api/poll_registration/?poll_id=${poll_id}`);
});
