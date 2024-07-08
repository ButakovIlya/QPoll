import { handleRequest } from '@/api/api';
import { createEffect } from 'effector';

export const changeUserDataFx = createEffect(async ({ user_id, field, value }) => {
  await handleRequest('patch', `/api/my_profile/?user_id=${user_id}`, {
    [field]: value,
  });
});
