import { Navigate, Outlet, useLocation } from 'react-router-dom';

import useAuth from '@/hooks/useAuth';
import { useUserRole } from '@/hooks/useUserRole';

const AdminPrivateRoute = () => {
  const { isAuthenticated } = useAuth();
  const { role } = useUserRole();
  const location = useLocation();

  return isAuthenticated === true && role === 'Администратор' ? (
    <Outlet />
  ) : (
    <Navigate to="/app" state={{ from: location }} replace />
  );
};

export default AdminPrivateRoute;
