import { handleRequest } from '@/api/api';
import { createEffect } from 'effector';

export const connect2AuthFx = createEffect(async ({ setQrCode }) => {
  await handleRequest('get', '/qr_code_view/').then((qr) => setQrCode(qr.data.qr_code));
});
