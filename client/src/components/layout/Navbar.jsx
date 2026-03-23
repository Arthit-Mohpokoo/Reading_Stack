import { useEffect, useState } from "react"
import { useSelector } from "react-redux"
import { useDispatch } from "react-redux"
import { useNavigate } from "react-router-dom"


function Navbar() {
    const user = useSelector((state) => state.user.user)
    const nav = useNavigate()

    const Logo = () => (
        <button className="font-serif xl:text-xl sm:text-lg" onClick={()=>nav("/")}>E-Reading</button>
    )

    const NavLink= ({label,path}) =>(
        <li onClick={()=>nav(path)} className="flex sm:text-xl p-2 cursor-pointer transition-colors duration-200 xl:text-xl">
            {label}
        </li>
    )
    return (
        <div className="w-100% ">
            <div className="flex justify-between ">
                <Logo />
                <ul className="flex">
                    <NavLink label="หน้าเเรก" path="/"/>
                    <NavLink label="Vocabulary" path="/Vocabulary"/>
                </ul>
            </div>
        </div>
    )


}

export default Navbar