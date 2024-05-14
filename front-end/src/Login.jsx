import { Navigate, useNavigate } from "react-router-dom";

const Login = () => {

    let navigate = useNavigate();
    const homeRoute = () => {
        let path = '/home';
        navigate(path);
    }

    const signUpRoute = () => {
        let path = '/signup';
        navigate(path);
    }

    return (
        <div className="bg-gray-100 p-4 h-screen flex justify-center items-center">
            <div className="bg-white rounded-2xl p-10 w-1/3 flex-col space-y-10">

                <div id="heading flex-col">
                    <p className="text-3xl text-indigo-900 font-bold">BREWBUCKS</p> 
                </div>

                <div id="input" className="flex-col space-y-2">
                    <div className="">
                        <input type="text" placeholder="Username" class="input input-bordered input-sm w-full max-w-md" />
                    </div>
                    <div>
                        <input type="text" placeholder="Password" class="input input-bordered input-sm w-full max-w-md" />
                    </div>
                </div>

                <div id="Buttons" className="flex-col space-y-2">
                    <div className="flex-col space-y-2">
                        <button onClick={homeRoute} className="btn btn-sm rounded-lg bg-indigo-900 p-2 content-center w-1/3">
                            <p className="text-white">
                                Login
                            </p>
                        </button> 
                        <div className="text-xs font-semibold flex space-x-1">
                            <p className="">Not a member?</p><a className="text-indigo-900" href="" onClick={signUpRoute}>Sign Up</a>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    )
}

export default Login;