import { handleRequest } from '@/api/api';

export const changePollTypeFx = async (id, q_id, type) => {
  return handleRequest(
    'patch',
    `/api/my_poll_question/?poll_id=${id}&poll_question_id=${q_id}`,
    type
  );
};
