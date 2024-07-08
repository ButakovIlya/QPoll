import { createEffect, createEvent, createStore } from 'effector';

import { handleRequest } from '@/api/api';

const updateCache = createEvent();
const requestQueue = new Map();

const initialCache = JSON.parse(localStorage.getItem('pollDataCache') || '{}');

export const pollDataCache = createStore(initialCache).on(
  updateCache,
  (state, { pollId, data }) => {
    const newState = { ...state, [pollId]: data };
    localStorage.setItem('pollDataCache', JSON.stringify(newState));
    return newState;
  },
);

// pollDataCache.watch((state) => console.log(state));

export const fetchPollDataFx = createEffect(async (pollId) => {
  // const currentCache = pollDataCache.getState();

  // if (currentCache[pollId]) return currentCache[pollId];

  // if (requestQueue.has(pollId)) return requestQueue.get(pollId);

  const fetchPromise = handleRequest('get', `/api/my_poll/?poll_id=${pollId}&detailed=0`)
    .then(({ data }) => {
      if (data) {
        updateCache({ pollId, data });
        return data;
      }
    })
    .finally(() => {
      requestQueue.delete(pollId);
    });

  requestQueue.set(pollId, fetchPromise);

  return fetchPromise;
});

export const pollDataStore = createStore({}).on(fetchPollDataFx.doneData, (_, data) => data);

export const pollStatusStore = pollDataStore.map((data) => data.is_in_production);
export const pollTypeStore = pollDataStore.map((data) => data.poll_type && data.poll_type.name);
export const isMultipleStore = pollDataStore.map((data) => data.has_multiple_choices);
