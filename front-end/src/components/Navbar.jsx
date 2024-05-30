import AvatarMenu from "./AvatarMenu";
import { Navigate, useNavigate } from "react-router-dom";
import Button from "./Button";

const Navbar = ({user}) => {
    let navigate = useNavigate();

    const username = user

    const homeRoute = () => {
        let path = '/home';
        navigate(path, {state:{username: username}})
    }

    const ordersRoute = () => {
        let path = '/orders';
        navigate(path, {state:{username: username}});
    }


    return (
        <div className="sticky top-0 z-50 shadow-md bg-white p-3">
            <div className="flex items-center space-x-3 justify-between pl-8 pr-8">
                <p className="text-3xl text-indigo-900 font-bold">BREWBUCKS</p> 
                <div className="flex space-x-8 items-center">
                    <div className="flex space-x-2">
                        <Button click={homeRoute} text={"Home"} width={"100%"}></Button>
                        <Button click={ordersRoute} text={"Orders"} width={"100%"}></Button>
                    </div>
                    <div className="flex items-center space-x-2">
                        <AvatarMenu username={username}points={99999}></AvatarMenu>
                        
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Navbar;