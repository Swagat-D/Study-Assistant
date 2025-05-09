import { createContext, useState, useEffect, useContext } from 'react';
import api from '../services/api';

// Create the auth context
export const AuthContext = createContext({
  user: null,
  isAuthenticated: false,
  isLoading: true,
  login: () => {},
  logout: () => {},
  register: () => {},
  error: null,
});

// Auth provider component
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Check if auth is enabled in .env
  const isAuthEnabled = import.meta.env.VITE_AUTH_ENABLED === 'true';
  
  useEffect(() => {
    // If auth is disabled, set a default user and skip authentication
    if (!isAuthEnabled) {
      setUser({ 
        id: '1', 
        name: 'Demo User', 
        email: 'demo@example.com', 
        role: 'user' 
      });
      setIsLoading(false);
      return;
    }
    
    // Check for existing token and load user data
    const checkAuth = async () => {
      const token = localStorage.getItem('token');
      
      if (!token) {
        setIsLoading(false);
        return;
      }
      
      try {
        // Try to get the user profile using the token
        const response = await api.get('/auth/profile');
        setUser(response.data);
      } catch (error) {
        console.error('Authentication error:', error);
        localStorage.removeItem('token');
      } finally {
        setIsLoading(false);
      }
    };
    
    checkAuth();
  }, [isAuthEnabled]);
  
  // Login function
  const login = async (email, password) => {
    setError(null);
    
    try {
      const response = await api.post('/auth/login', { email, password });
      const { token, user } = response.data;
      
      // Save token and user data
      localStorage.setItem('token', token);
      setUser(user);
      
      return true;
    } catch (error) {
      setError(error.response?.data?.message || 'Login failed. Please check your credentials.');
      return false;
    }
  };
  
  // Register function
  const register = async (name, email, password) => {
    setError(null);
    
    try {
      const response = await api.post('/auth/register', { name, email, password });
      const { token, user } = response.data;
      
      // Save token and user data
      localStorage.setItem('token', token);
      setUser(user);
      
      return true;
    } catch (error) {
      setError(error.response?.data?.message || 'Registration failed. Please try again.');
      return false;
    }
  };
  
  // Logout function
  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };
  
  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        logout,
        register,
        error,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

// Custom hook for using auth context
export function useAuth() {
  return useContext(AuthContext);
}

export default AuthContext;