import './App.css';
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LandPage from './pages/LandPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandPage />} />

      </Routes>
    </BrowserRouter>
  );
}

export default App;
