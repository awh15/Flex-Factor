import React from 'react'; 
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'; // Changed to BrowserRouter
import Navbar from './features/navbar/Navbar';
import HomePage from './features/homepage/HomePage';
import SignUp from './features/signup/Signup';
import './App.css';    
import Login from './features/login/Login';
 

function App() {
  return (
    <Router> {/* Changed to BrowserRouter */}
      <div className='App'>
        <Navbar />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
