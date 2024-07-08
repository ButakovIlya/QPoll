import { handleRequest } from '@/api/api';
import { createEffect } from 'effector';

export const getAllUsersFx = createEffect(async () => {
  const data = await handleRequest('get', `/admin_api/users/`);
  return data;
});
