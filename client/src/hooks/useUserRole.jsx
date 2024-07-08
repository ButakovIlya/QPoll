import { useContext } from 'react';

import UserRoleContext from '@/app/context/UserRoleProvider';

export const useUserRole = () => useContext(UserRoleContext);
