import { handleRequest } from '@/api/api';
import { createEffect } from 'effector';

export const closePollFx = createEffect(async (poll_id) => {
  await handleRequest('patch', `/api/my_poll/?poll_id=${poll_id}`, {
    is_closed: true,
  });
});
