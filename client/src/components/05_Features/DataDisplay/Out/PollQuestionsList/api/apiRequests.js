import { handleRequest } from '@/api/api';

export const deleteQuestionRequest = async (id, q_id) => {
  return handleRequest('delete', `/api/my_poll_question/?poll_id=${id}&poll_question_id=${q_id}`);
};
