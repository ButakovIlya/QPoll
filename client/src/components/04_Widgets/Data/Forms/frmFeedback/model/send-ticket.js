import { createEffect } from 'effector';

import { handleRequest } from '@/api/api';

export const sendTicketFx = createEffect(async ({ type, message }) => {
  await handleRequest('post', `/api/my_support_requests/`, {
    ticket_type: type,
    text: message,
  });
});
