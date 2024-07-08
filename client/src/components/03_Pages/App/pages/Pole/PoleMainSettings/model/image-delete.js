import { handleRequest } from '@/api/api';
import { createEffect } from 'effector';

export const deleteImageFx = createEffect(async ({ id }) => {
  await handleRequest('put', `/api/my_poll/?poll_id=${id}&request_type=delete_image`, {
    image: null,
  });
});
