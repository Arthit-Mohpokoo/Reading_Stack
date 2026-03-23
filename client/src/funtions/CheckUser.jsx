import { useEffect } from "react"
import { useDispatch, useSelector } from "react-redux"
import { Navigate, Outlet } from "react-router-dom"
import { login_c, logout, setloading } from "../store/checktoken"
import { currenuser } from "./auth"

function CheckUser({ children }) {
    const user = useSelector((state) => state.user.user)
    const load = useSelector((state) => state.user.loading)
    if (load) return <div>Loading...</div>
    if (!user || !user.role) return <Navigate to="/index" replace />
    return <Outlet />
}
export default CheckUser