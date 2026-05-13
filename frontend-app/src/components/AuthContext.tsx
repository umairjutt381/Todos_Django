import React, { createContext, useState, useCallback, useEffect } from 'react';
import { User } from '../types';
import { authService } from '../services/api';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, password: string, email?: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
  isAdmin: boolean;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Function to get CSRF token from backend
async function initializeCsrf() {
  try {
    await fetch('http://localhost:8000/api/auth/me/', {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Accept': 'application/json',
      }
    }).catch(() => {
      // This will fail if not authenticated, which is expected
    });
  } catch (error) {
    // Ignore errors - just initializing CSRF
  }
}

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Initialize CSRF token and check if user is logged in
    const checkAuth = async () => {
      try {
        await initializeCsrf();
        const userData = await authService.login();
        setUser(userData);
      } catch {
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const login = useCallback(async (username: string, password: string) => {
    setLoading(true);
    try {
      await initializeCsrf();
      const response = await authService.login({ username, password });
      setUser({
        id: response.id,
        username: response.username,
        email: response.email,
        is_admin: response.is_admin,
      });
    } finally {
      setLoading(false);
    }
  }, []);

  const register = useCallback(async (username: string, password: string, email?: string) => {
    setLoading(true);
    try {
      await initializeCsrf();
      // Just register, don't auto-login - let user go to login page
      await authService.register({ username, password, email });
      // Return success - caller will redirect to login
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = useCallback(() => {
    authService.logout().catch(console.error);
    setUser(null);
  }, []);

  const value: AuthContextType = {
    user,
    loading,
    login,
    register,
    logout,
    isAuthenticated: !!user,
    isAdmin: user?.is_admin || false,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = React.useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

