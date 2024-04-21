import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css'; // Importing the CSS file

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar__left">
        <Link to="/" className="navbar__logo">Flex Factor</Link>
      </div>
      <div className="navbar__right">
        <Link to="/login" className="navbar__button">Login</Link>
        <Link to="/signup" className="navbar__button">Sign Up</Link>
      </div>
    </nav>
  );
}

export default Navbar;
