import { handleRequest } from '@/api/api';
import { createEffect } from 'effector';

export const publishPollFx = createEffect(async ({ id }) => {
  const data = await handleRequest(
    'put',
    `/api/my_poll/?poll_id=${id}&request_type=deploy_to_production`
  );
  return data.data;
});
