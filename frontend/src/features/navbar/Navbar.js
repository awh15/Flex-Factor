import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css'; // Importing the CSS file
import { useSelector } from 'react-redux';
import { useDispatch } from 'react-redux';
import { logout } from '../login/loginSlice';

const Navbar = () => {
  const dispatch = useDispatch();
  const { isAuthenticated } = useSelector(state => state.login);

  return (
    <nav className="navbar">
      <div className="navbar__left">
        <Link to="/" className="navbar__logo">Flex Factor</Link>
      </div>
      <div className="navbar__right">
        {isAuthenticated ? (
          <button className="navbar__button" onClick={()=>{dispatch(logout())}}>Logout</button>
        ) : (
          <>
            <Link to="/login" className="navbar__button">Login</Link>
            <Link to="/signup" className="navbar__button" >Sign Up</Link>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
