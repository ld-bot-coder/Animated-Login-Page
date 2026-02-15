import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import apiService from '../services/api';
import logo from '../assets/images/logo.png';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    if (isLoggedIn === 'true') {
      navigate('/dashboard');
    }
  }, [navigate]);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await apiService.login(email, password);

      // Store token and user info
      localStorage.setItem('token', response.token);
      localStorage.setItem('isLoggedIn', 'true');
      localStorage.setItem('role', response.user.role);
      localStorage.setItem('email', response.user.email);

      // Navigate based on role
      if (response.user.role === 'admin') {
        navigate('/admin');
      } else {
        navigate('/dashboard');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  const handleRegisterRedirect = () => {
    navigate('/signup');
  };

  return (
    <>
      {/* Simple Navbar with just logo */}
      <nav className="bg-white text-black p-2 flex items-center border-b border-gray-300 h-16 fixed top-0 left-0 right-0 z-50">
        <div className="flex items-center">
          <img src={logo} alt="Logo" className="w-32 h-8 ml-16" />
        </div>
      </nav>

      {/* Login Content */}
      <div
        className="flex items-center justify-center min-h-screen bg-gray-100 pt-16"
        style={{
          backgroundImage: 'url(https://s3-alpha-sig.figma.com/img/3bea/8a87/26fbf8711df83b40ea54d869a307e803?Expires=1725840000&Key-Pair-Id=APKAQ4GOSFWCVNEHN3O4&Signature=cr0IgeIuCKUGACdQ4N9hUxKNkkJlnEepP0wP5Pb~1ro~b8h3lEGidetZ433PPct5w-BuQNERpvjY26c0SWnz8mody1l~X0CBWJ-gZJ2Llm5BX9mfcFj1K9e2UYssZIzGaBAA5lmTOq58hqHWYBDTxjwSACtvAd-Gn9c9crJ16shBkFq4hpzZuWOR8WYIPMmd5CNJnZgND8vd0kzIBlUacTp59FDtKzM7pMY6JKHNiwjQTXK2PsnJ8HdR~kckTGhqb281murtxGrChVwX4dU29yjXItEtHF1KI~vUh3B1MDJhaUmtjUY4LGu0Gdn6arGu4e7fE2NC7YxieDPJRPftbQ__)',
          backgroundSize: 'cover',
          backgroundPosition: 'center'
        }}
      >
        <div className="w-full max-w-md bg-white shadow-md rounded-lg p-8">
          <h2 className="text-2xl font-semibold text-center text-gray-700 mb-6">Login</h2>
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
            <div>
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
            {error && <p className="text-red-500 text-sm">{error}</p>}
            <button
              type="submit"
              disabled={loading}
              className="w-full font-semibold py-2 rounded-lg transition duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
              style={{
                color: 'white',
                backgroundColor: '#7C3A84'
              }}
            >
              {loading ? 'Logging in...' : 'Login'}
            </button>


          </form>
          <div className="mt-4 text-center">
            {/* <p className="text-gray-600">Need Help?</p> */}

          </div>
        </div>
      </div>
    </>
  );
};

export default Login;
