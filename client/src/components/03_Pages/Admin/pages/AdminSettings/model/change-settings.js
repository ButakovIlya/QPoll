import { createEffect } from 'effector';

import { handleRequest } from '@/api/api';

export const changeSettingsFx = createEffect(async ({ link, value }) => {
  const data = await handleRequest('patch', `/admin_api/project_settings/?poll_id=1`, {
    [link]: value,
  });
  return data.data;
});
