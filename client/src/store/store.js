import { configureStore } from "@reduxjs/toolkit";
import todosSlice from "./checktoken"

const store = configureStore({
    reducer:{
        user:todosSlice
    }
})

export default store;