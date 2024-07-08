import { createEffect } from 'effector';

import { handleRequest } from '@/api/api';

export const applyFiltersFx = createEffect(async ({ filters, setPolls }) => {
  const cleanedFilters = Object.fromEntries(
    Object.entries(filters)
      .filter(([key, value]) => value !== '' && value !== 'Все типы')
      .map(([key, value]) => [key, typeof value === 'boolean' ? (value ? 1 : 0) : value]),
  );
  const queryParams = new URLSearchParams(cleanedFilters).toString();

  await handleRequest('get', `/api/poll/?${queryParams}`).then((res) => setPolls(res.data.results));
});
