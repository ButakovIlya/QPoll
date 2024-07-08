import { createEffect } from 'effector';

import { handleRequest } from '@/api/api';

export const getTicketsFx = createEffect(async () => {
  const data = await handleRequest('get', `/admin_api/support_request/`);
  return data.data;
});
