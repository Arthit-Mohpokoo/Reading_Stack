import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { register, login } from "../../funtions/auth";
import { useDispatch } from "react-redux";
import { login_c } from "../../store/checktoken";

const Singup = () => {
  const nav = useNavigate();
  const [errc, seterrc] = useState("")
  const dispatch = useDispatch()

  const seterrcAuto = (msg) => {
    seterrc(msg)
    setTimeout(() => seterrc(""), 3000)
  }

  const handleSubmitRegis = async (e) => {
    e.preventDefault();
    const data = new FormData(e.currentTarget);
    const getform = {
      email: data.get("email"),
      password: data.get("password"),
      conpass: data.get("con_password"),
    };
    if (!getform.email || !getform.password || !getform.conpass)
      return seterrcAuto("กรุณากรอกข้อมูลให้ครบ");
    if (getform.password !== getform.conpass)
      return seterrcAuto("รหัสผ่านไม่ตรงกัน");
    try {
      await register(getform);
      seterrcAuto("สมัครเสร็จสิ้น")
    } catch (err) {
      seterrcAuto(err.response?.data?.detail || "เกิดข้อผิดพลาด")
    }
  };

  const handleSubmitlogin = async (e) => {
    e.preventDefault();
    try {
      const data = new FormData(e.currentTarget);
      const getform = {
        email: data.get("email"),
        password: data.get("password")
      }
      if (!getform.email || !getform.password)
        return seterrcAuto("กรุณากรอกข้อมูลให้ครบ");
      const res = await login(getform)
      dispatch(login_c({
        email: res.data.email,
        role: res.data.role,
        token: res.data.token,
      }))
      localStorage.setItem("token", res.data.token)
      localStorage.setItem("user", JSON.stringify(res.data))
      if (res.data.role === "admin") {
        nav("/dashboard/Admin")
      } else {
        nav("/")
      }
    } catch (err) {
      seterrcAuto(err.response?.data?.detail || "เกิดข้อผิดพลาด")
    }
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">

      {errc && (
        <div className={`flex items-center gap-2 px-4 py-2 mb-4 rounded border ${
          errc === "สมัครเสร็จสิ้น"
            ? "bg-green-100 border-green-500 text-green-700"
            : "bg-red-100 border-red-500 text-red-700"
        }`}>
          <span className="text-lg font-bold">
            {errc === "สมัครเสร็จสิ้น" ? "✓" : "✕"}
          </span>
          <span>{errc}</span>
        </div>
      )}

      <div className="flex gap-8">
        <div className="bg-white p-6 rounded shadow w-72">
          <h2 className="text-xl font-bold mb-4">สมัครสมาชิก</h2>
          <form onSubmit={handleSubmitRegis} className="flex flex-col gap-3">
            <input name="email" type="email" placeholder="Your Email"
              className="border rounded px-3 py-2 outline-none focus:border-blue-400" />
            <input name="password" type="password" placeholder="Password"
              className="border rounded px-3 py-2 outline-none focus:border-blue-400" />
            <input name="con_password" type="password" placeholder="Confirm Password"
              className="border rounded px-3 py-2 outline-none focus:border-blue-400" />
            <button type="submit"
              className="bg-blue-500 text-white py-2 rounded hover:bg-blue-600">
              สมัคร
            </button>
          </form>
        </div>

        <div className="bg-white p-6 rounded shadow w-72">
          <h2 className="text-xl font-bold mb-4">เข้าสู่ระบบ</h2>
          <form onSubmit={handleSubmitlogin} className="flex flex-col gap-3">
            <input name="email" type="email" placeholder="Your Email"
              className="border rounded px-3 py-2 outline-none focus:border-blue-400" />
            <input name="password" type="password" placeholder="Password"
              className="border rounded px-3 py-2 outline-none focus:border-blue-400" />
            <button type="submit"
              className="bg-green-500 text-white py-2 rounded hover:bg-green-600">
              เข้าสู่ระบบ
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Singup;