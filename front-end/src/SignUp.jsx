import { Navigate, useNavigate } from "react-router-dom";

const SignUp = () => {

    let navigate = useNavigate();
    const routeChange = () => {
        let path = '/';
        navigate(path);
    }

    return (
        <div className="bg-gray-100 p-4 h-screen flex justify-center items-center">
            <div className="bg-white rounded-2xl p-10 w-1/3 flex-col space-y-10">

                <div id="heading flex-col">
                    <p className="text-3xl text-indigo-900 font-bold">JOIN BREWBUCKS</p> 
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
                        <button onClick={routeChange} className="btn btn-sm rounded-lg bg-indigo-900 p-2 content-center w-1/3">
                            <p className="text-white ">
                                Sign Up
                            </p>
                        </button> 
                    </div>
                </div>

            </div>
        </div>
    )
}

export default SignUp;