import { handleRequest } from '@/api/api';

export const deleteImageFx = async ({ id, q_id }) => {
  return handleRequest(
    'put',
    `/api/my_poll_question/?poll_id=${id}&poll_question_id=${q_id}&request_type=delete_image`,
    {
      image: null,
    }
  );
};
