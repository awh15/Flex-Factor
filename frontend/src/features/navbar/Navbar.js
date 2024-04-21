import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css'; // Importing the CSS file
import { useSelector } from 'react-redux';
import { useDispatch } from 'react-redux';
import { logout, getRole } from '../login/loginSlice';
import { UserRole } from '../../constants/Constants';

const Navbar = () => {
  const dispatch = useDispatch();
  const { isAuthenticated, token, role } = useSelector(state => state.login);
  
  useEffect(()=>{
    if(!token){
      return; 
    }
    dispatch(getRole());
  },[token, role]);

  return (
    <nav className="navbar">
      <div className="navbar__left">
        <Link to="/" className="navbar__logo">Flex Factor</Link>
      </div>
      <div className="navbar__right">
        {isAuthenticated ? (
          <>
            {role === UserRole.END_USER && (
              <>
                <Link to="/profile" className="navbar__item">Profile</Link>
              </>
            )}
            {role === UserRole.VENDOR && (
              <>
                <Link to="/dashboard" className="navbar__item">Dashboard</Link>
              </>
            )}
            {role === UserRole.ADMIN && (
              <> 
                <Link to="/analytics" className="navbar__item">Analytics</Link>
              </>
            )}
            <button className="navbar__button" onClick={()=>{dispatch(logout())}}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login" className="navbar__item">Login</Link>
            <Link to="/signup" className="navbar__button">Sign Up</Link>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
