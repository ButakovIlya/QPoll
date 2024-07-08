import { handleRequest } from '@/api/api';
import { createEffect } from 'effector';
import { v4 } from 'uuid';

export const duplicatePollFx = createEffect(async (poll_id) => {
  await handleRequest('put', `/api/my_poll/?request_type=clone_poll&poll_id=${poll_id}`, {
    new_poll_id: v4(),
  });
});
