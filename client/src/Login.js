import React, { useState } from 'react';
import axios from 'axios';
import './Login.css';

function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);

  const handleLogin = async () => {
    if (!username || !password) {
      setError('Please enter both username and password.');
      return;
    }

    try {
      const response = await axios.post('/api/login', {
        username,
        password,
      }, {
        headers: { 'Content-Type': 'application/json' },
      });
      onLogin(response.data.user_id, response.data.username, response.data.history);
    } catch (err) {
      setError('Login failed. Please try again.');
      console.error('Login error:', err.response?.data || err.message);
    }
  };

  return (
    <div className="login-container">
      <h2>Login to MedGenie</h2>
      <div className="login-form">
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={handleLogin}>Login</button>
        {error && <div className="error">{error}</div>}
      </div>
    </div>
  );
}

export default Login;