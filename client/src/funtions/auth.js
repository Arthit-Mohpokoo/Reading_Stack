import axios from "axios";

export const login = async (data) => {
  return await axios.post(import.meta.env.VITE_API_URL + "/login", data);
};
export const register = async (data) => {
  console.log(import.meta.env.VITE_API_URL);
  return await axios.post(import.meta.env.VITE_API_URL + "/register", data);
};

export const currenuser = async (token) => {
  return await axios.get(import.meta.env.VITE_API_URL + "/curren-user", {
    headers: { Authorization: `Bearer ${token}` },
  });
};
