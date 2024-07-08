import { createEffect } from 'effector';

import { handleRequest } from '@/api/api';

export const getRemainingTimeFx = createEffect(async ({ id, formId }) => {
  const response = await handleRequest(
    'get',
    `/api/poll_voting_started/?poll_id=${id}${formId ? `&poll_answer_group_id=${formId}` : ''}`,
  );
  return response.data.data;
});
