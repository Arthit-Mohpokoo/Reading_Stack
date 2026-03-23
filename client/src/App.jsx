import { useEffect, useState } from 'react'
import { BrowserRouter, Route, Routes } from "react-router-dom";
import './App.css'
import Singup from './components/auth/Singup';
import { currenuser } from './funtions/auth';
import { useDispatch } from 'react-redux';
import { login_c } from './store/checktoken';
import Home from './components/pages/Home';
import CheckUser from './funtions/CheckUser'
import { setloading } from './store/checktoken';
import Vocabulary from './components/pages/Vocabulary';

function App() {
  const dispatch = useDispatch()
  useEffect(() => {
    const token = localStorage.getItem("token")
    if (token && token !== "null") {
        currenuser(token)
            .then((res) => {
                dispatch(login_c({
                    email: res.data.email,
                    role: res.data.role,
                    token: token
                }))
            })
            .catch(() => {
                localStorage.removeItem("token")
            })
            .finally(() => {
                dispatch(setloading(false))
            })
    } else {
        dispatch(setloading(false))
    }
}, [])
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path='/index' element={<Singup />} />
          <Route element={<CheckUser />}>
            <Route path='/' element={<Home />} />
            <Route path='/Vocabulary' element={<Vocabulary />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App
