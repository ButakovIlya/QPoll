import { handleRequest } from '@/api/api';
import { createEffect } from 'effector';

export const deletePollFx = createEffect(async (poll_id) => {
  await handleRequest('delete', `/api/my_poll/?poll_id=${poll_id}`);
});
