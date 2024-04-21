import React from 'react'; 
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'; // Changed to BrowserRouter
import Navbar from './features/navbar/Navbar';
import './App.css'; // Import the CSS file

function Home() {
  return <h1>Welcome to Flex Factor</h1>;
}

function Login() {
  return <h1>Login Page</h1>;
}

function SignUp() {
  return <h1>Sign Up Page</h1>;
}

function App() {
  return (
    <Router> {/* Changed to BrowserRouter */}
      <div className='App'>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
