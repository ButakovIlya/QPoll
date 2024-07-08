import { useEffect, useState } from 'react';

import useAuth from './useAuth';
import { useUserRole } from './useUserRole';

import { handleRequest } from '@/api/api';

const useUserData = () => {
  const { setUserRole } = useUserRole();
  const { isAuthenticated, token } = useAuth();
  const [userData, setUserData] = useState({});

  useEffect(() => {
    const fetchUserData = async () => {
      if (!isAuthenticated) {
        return;
      }

      const headers = {
        Authorization: `Token ${token}`,
      };
      const { data } = await handleRequest('get', '/api/my_profile/', null, headers);
      setUserRole(data.role);
      setUserData(data);
    };

    fetchUserData();
  }, []);

  return userData;
};

export default useUserData;
