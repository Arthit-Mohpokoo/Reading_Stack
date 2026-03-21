import { useState } from 'react'
import { BrowserRouter, Route, Routes } from "react-router-dom";

import './App.css'
import Singing from './components/auth/singing';
import Singup from './components/auth/Singup';

function App() {

  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path='/login' element={<Singing/>}/>
          <Route path='/' element={<Singup/>}/>
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App
