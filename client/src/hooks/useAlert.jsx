import { useContext } from 'react';

import AlertContext from '@/app/context/AlertProvider';

export const useAlert = () => {
  return useContext(AlertContext);
};
