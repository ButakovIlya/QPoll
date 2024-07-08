import { handleRequest } from '@/api/api';
import { createEffect } from 'effector';

export const copyQuestionFx = createEffect(async ({ id, q_id }) => {
  const newQue = await handleRequest(
    'put',
    `/api/my_poll_question/?request_type=copy_question&poll_id=${id}&poll_question_id=${q_id}`
  );
  return newQue.data;
});
