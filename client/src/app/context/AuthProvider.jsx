import { createContext, useCallback, useEffect, useMemo, useState } from 'react';

const AuthContext = createContext({
  isAuthenticated: false,
  setAuth: () => {},
});

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [token, setToken] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const storedToken = localStorage.getItem('auth_token');
    if (storedToken) {
      setIsAuthenticated(true);
      setToken(storedToken);
    }
    setIsLoading(false);
  }, []);

  const setAuth = useCallback(
    (newToken) => {
      if (newToken && typeof newToken === 'string') {
        setIsAuthenticated(true);
        setToken(newToken);
        localStorage.setItem('auth_token', newToken);
      } else {
        setIsAuthenticated(false);
        setToken('');
        localStorage.removeItem('auth_token');
      }
    },
    [setIsAuthenticated, setToken],
  );

  const contextValue = useMemo(
    () => ({ isAuthenticated, setAuth, token, isLoading }),
    [isAuthenticated, setAuth],
  );

  return <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>;
};

export default AuthContext;
