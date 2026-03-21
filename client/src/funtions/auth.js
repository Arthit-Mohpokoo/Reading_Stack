import axios from "axios";

export const login = async(req,res) =>{
    return (await axios.post(import.meta.URLBE + "/login"))
}
export const register = async(req,res) =>{
    return (await axios.post(import.meta.URLBE + "/register"))
}