import { createEffect } from 'effector';

import { handleRequest } from '@/api/api';

export const sendAnswersRequestFx = createEffect(async ({ answers, id, isTimeEnd, formId }) => {
  const response = await handleRequest(
    'post',
    `/api/poll_voting${isTimeEnd ? '_ended' : ''}/?poll_id=${id}${formId ? `&poll_answer_group_id=${formId}` : ''}`,
    {
      answers: answers,
    },
  );
  return response.data;
});
