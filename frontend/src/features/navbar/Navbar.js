import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css'; // Importing the CSS file
import { useSelector } from 'react-redux';
import { useDispatch } from 'react-redux';
import { logout, getRole } from '../login/loginSlice';
import { UserRole } from '../../constants/Constants';

const Navbar = () => {
  const dispatch = useDispatch();
  const { isAuthenticated, token } = useSelector(state => state.login);
  const [userRole, setUserRole] = useState(UserRole.END_USER);

  useEffect(() => {
    const fetchData = async () => {
      if (token && isAuthenticated) {
        const role = await dispatch(getRole());
        if (role !== UserRole.END_USER) {
          setUserRole(role);
        }
      }
    };
  
    fetchData(); // Call the async function immediately
  
  }, [token, dispatch]);
  

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
