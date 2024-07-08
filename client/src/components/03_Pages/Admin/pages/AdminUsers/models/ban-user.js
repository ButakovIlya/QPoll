import { createEffect } from 'effector';

import { handleRequest } from '@/api/api';

export const banUserFx = createEffect(async ({ id, status }) => {
  const data = await handleRequest('patch', `/admin_api/users/?user_id=${id}`, {
    is_banned: status,
  });
  return data.data;
});
