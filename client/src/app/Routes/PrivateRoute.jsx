import useAuth from '@hooks/useAuth';
import { useEffect, useState } from 'react';
import { Navigate, Outlet, useLocation } from 'react-router-dom';

export const PrivateRoute = () => {
  const location = useLocation();
  const { isAuthenticated } = useAuth();
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    let isMounted = true;

    const checkToken = async () => {
      try {
        const storedToken = localStorage.getItem('auth_token');
        if (isMounted && storedToken) setIsReady(true);
      } catch (error) {
        console.error('Error while checking token:', error);
      }
    };

    checkToken();

    return () => {
      isMounted = false;
    };
  }, []);

  const renderContent = () => {
    if (!isReady) return null;

    if (!isAuthenticated) {
      return <Navigate to="/signin" state={{ from: location }} replace />;
    }
    return <Outlet />;
  };

  return renderContent();
};
