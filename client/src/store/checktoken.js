import { createSlice } from '@reduxjs/toolkit'
import { login } from '../funtions/auth'
import { act } from 'react';

const initialState ={
    value : "getoken",
    user:null,
    loading:true,
}


const todosSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    login_c: (state,actions)=>{
        state.value = "singin";
        state.user = actions.payload;
        state.loading = false
    },
    logout: (state)=>{
        state.user = null;
        state.loading = false
        localStorage.removeItem("token");
        localStorage.removeItem("user")
    },
    setloading:(state,actions)=>{
        state.loading = actions.payload
    }
  }
})

export const {login_c, logout, setloading} = todosSlice.actions
export default todosSlice.reducer