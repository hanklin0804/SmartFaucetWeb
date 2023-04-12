import { BrowserRouter, Routes, Route } from "react-router-dom";
import LoginPage from './pages/login/LoginPage';
import HomePage from './pages/home/HomePage';
import SignPage from './pages/signup/SignupPage';
import React from 'react';
import { useSelector } from 'react-redux';

function App() {
  // const isLoggedIn = useSelector((state) => state.auth.isLoggedIn);
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/signup" element={<SignPage />} />
      </Routes>
    </BrowserRouter>

  );
}

export default App;
