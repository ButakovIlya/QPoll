import { createEffect } from 'effector';

import { handleRequest } from '@/api/api';

export const getSettingsFx = createEffect(async () => {
  const data = await handleRequest('get', `/admin_api/project_settings/`);
  return data.data;
});
