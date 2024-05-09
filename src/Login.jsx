import { Navigate, useNavigate } from "react-router-dom";

const Login = () => {

    let navigate = useNavigate();
    const routeChange = () => {
        let path = '/home';
        navigate(path);
    }

    return (
        <div className="bg-gray-100 p-4 h-screen flex justify-center items-center">
            <div className="bg-white rounded-2xl p-4 w-1/3 h-2/3">
                <div className="flex-col space-y-4">
                    <div>
                        <p className="text-3xl text-indigo-900 font-bold">BREWBUCKS</p> 
                    </div>
                    <div className="">
                        <input type="text" placeholder="Username" class="input input-bordered input-sm w-full max-w-md" />
                    </div>
                    <div>
                        <input type="text" placeholder="Password" class="input input-bordered input-sm w-full max-w-md" />
                    </div>
                    <div className="flex-col space-y-0.5">
                        <button onClick={routeChange} className="btn btn-sm rounded-lg bg-indigo-900 p-2 content-center w-1/3">
                            <p className="text-white">
                                Login
                            </p>
                        </button> 
                        <div>
                        <p className="text-sm">or</p>
                        </div>
                        <button onClick={routeChange} className="btn btn-sm rounded-lg bg-indigo-900 p-2 content-center w-1/3">
                            <p className="text-white">
                                Sign Up
                            </p>
                        </button> 
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Login;