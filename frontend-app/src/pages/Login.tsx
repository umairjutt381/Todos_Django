import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../components/AuthContext';
import './Auth.css';

export const Login: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const { login } = useAuth();

  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    setLoading(true);
    setError('');

    try {
      await login(username, password);

      navigate('/todos');
    } catch (err: any) {
      console.error(err);

      setError(
        err.response?.data?.error ||
          err.response?.data?.detail ||
          'Login failed'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-box">

        <h2>Login</h2>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>

          <div>
            <label>Username</label>

            <input
              type="text"
              value={username}
              placeholder="Enter username"
              onChange={(e) =>
                setUsername(e.target.value)
              }
              required
            />
          </div>

          <div>
            <label>Password</label>

            <input
              type="password"
              value={password}
              placeholder="Enter password"
              onChange={(e) =>
                setPassword(e.target.value)
              }
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
          >
            {loading
              ? 'Logging in...'
              : 'Login'}
          </button>

        </form>

        <p>
          Don't have an account?{' '}
          <a href="/register">
            Register here
          </a>
        </p>

      </div>
    </div>
  );
};