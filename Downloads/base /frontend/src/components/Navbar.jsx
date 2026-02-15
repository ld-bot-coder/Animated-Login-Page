// components/Navbar.jsx
import React from 'react';
import logo from "../assets/images/logo.png";

const Navbar = () => {
  return (
    <nav className="bg-white text-black p-2 flex items-center justify-between border-b border-gray-300 h-16">
      <div className="flex items-center">
        <img src={logo} alt="Logo" className="w-32 h-8 ml-16" />
      </div>

      <div className="flex items-center mr-5">
        <button
          onClick={() => {
            localStorage.removeItem('token');
            localStorage.setItem('isLoggedIn', 'false');
            window.location.href = '/login';
          }}
          className="text-white hover:opacity-80 text-sm px-6 py-2 rounded-lg transition duration-300"
          style={{ backgroundColor: '#7C3783' }}
        >
          Logout
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
