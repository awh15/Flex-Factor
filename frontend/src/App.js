import React from 'react'; 
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'; // Changed to BrowserRouter
import Navbar from './features/navbar/Navbar';
import HomePage from './features/homepage/HomePage';
import SignUp from './features/signup/Signup';
import Login from './features/login/Login';
import Analytics from './features/analytics/Analytics';
import Dashboard from './features/dashboard/Dashboard';
import Profile from './features/profile/Profile';
import ProductPage from './features/productpage/ProductPage';

import './App.css';

function App() {
  return (
    <Router>
      <div className='App'>
        <Navbar />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} /> 
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/product/:productId"element={<ProductPage/>}> </Route>
        </Routes>
      </div>
    </Router>
  );
}

export default App;
