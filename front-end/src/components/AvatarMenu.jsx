import Avatar from "./Avatar";
import { Navigate, useNavigate } from "react-router-dom";

const AvatarMenu = ({points, username}) => {
    let navigate = useNavigate();
    const routeChange = () => {
        let path = '/';
        navigate(path);
    }

    return (
        <div className="dropdown dropdown-hover dropdown-end">
            <Avatar tabIndex={0} role="button" className="btn m-1"></Avatar>
            <ul tabIndex={0} className="dropdown-content z-[1] menu p-2 space-y-1 shadow border-2 bg-gray-100 rounded-box w-52">
                <li><p className="font-semibold">{username}</p></li>
                <li><a className="font-semibold">{points} Reward Points</a></li>
                <li className="bg-indigo-900 rounded-lg"><a onClick={routeChange} className="w-full text-white font-semibold text-justify">Sign Out</a></li>
            </ul>
        </div>
    )
}

export default AvatarMenu;