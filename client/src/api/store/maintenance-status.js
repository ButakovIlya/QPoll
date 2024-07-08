import { createEvent, createStore } from 'effector';

export const setMaintenanceMode = createEvent();
export const $isMaintenanceMode = createStore(false).on(
  setMaintenanceMode,
  (state, payload) => payload,
);
