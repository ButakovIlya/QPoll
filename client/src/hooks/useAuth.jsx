import { useContext } from 'react';

import AuthContext from '@/app/context/AuthProvider';

function useAuth() {
  return useContext(AuthContext);
}

export default useAuth;
