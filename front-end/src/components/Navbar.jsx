import AvatarMenu from "./AvatarMenu";
import { Navigate, useNavigate } from "react-router-dom";

const Navbar = () => {
    let navigate = useNavigate();
    const homeRoute = () => {
        let path = '/home';
        navigate(path);
    }

    const ordersRoute = () => {
        let path = '/orders';
        navigate(path);
    }


    return (
        <div className="bg-white p-4">
            <div className="flex items-center space-x-3 justify-between pl-8 pr-8">
                <p className="text-3xl text-indigo-900 font-bold">BREWBUCKS</p> 
                <div className="flex space-x-4 items-center">
                    <div className="flex space-x-2">
                        <button onClick={homeRoute} className="btn btn-sm content-center bg-indigo-900">
                            <p className="font-bold text-white">Home</p>
                        </button>
                        <button onClick={ordersRoute} className="btn btn-sm content-center bg-indigo-900">
                            <p className="font-bold text-white">Orders</p>
                        </button>
                    </div>
                    <AvatarMenu points={99999}></AvatarMenu>
                </div>
            </div>
        </div>
    )
}

export default Navbar;