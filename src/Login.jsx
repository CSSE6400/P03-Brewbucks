import { Navigate, useNavigate } from "react-router-dom";

const Login = () => {

    let navigate = useNavigate();
    const routeChange = () => {
        let path = '/home';
        navigate(path);
    }

    return (
        <div className="bg-gray-100 p-4 h-screen flex justify-center items-center">
            <div className="bg-white rounded-lg p-4 w-1/3 h-2/3">
                <div className="flex-col  space-y-4">
                    <div className="">
                        <input type="text" placeholder="Username" class="input input-bordered input-md w-full max-w-xs border-indigo-900 border-2" />
                    </div>
                    <div>
                        <input type="text" placeholder="Password" class="input input-bordered input-md w-full max-w-xs border-indigo-900 border-2" />
                    </div>
                    <button onClick={routeChange}>
                        Log In
                    </button>
                </div>
            </div>
        </div>
    )
}

export default Login;