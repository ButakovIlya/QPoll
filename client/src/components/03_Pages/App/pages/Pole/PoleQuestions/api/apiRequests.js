import { handleRequest } from '@/api/api';

export const handleCreateQuestionRequest = async (id) => {
  return handleRequest('post', `/api/my_poll_question/`, { poll_id: id });
};

export const handleGetAllQuestionRequest = async (id) => {
  return handleRequest('get', `/api/my_poll_question/?poll_id=${id}`);
};

export const handleGetQuestionInfoRequest = async (id, q_id) => {
  return handleRequest('get', `/api/my_poll_question/?poll_id=${id}&poll_question_id=${q_id}`);
};
