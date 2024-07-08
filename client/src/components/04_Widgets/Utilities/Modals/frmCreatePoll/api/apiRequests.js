import { handleRequest } from '@/api/api';

export const createPole = async (poleType, poleId) => {
  return handleRequest(
    'post',
    '/api/my_poll/',
    { poll_type: poleType, poll_id: poleId },
    'Create_pole'
  );
};
