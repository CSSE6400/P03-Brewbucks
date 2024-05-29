import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Button from "./components/Button";
import Input from "./components/Input";
import Logo from "./images/logo.png";
import './styles.css';


const Login = () => {
    const [showSignUp, setShowSignUp] = useState(false);
    const navigate = useNavigate();

    const homeRoute = () => {
        let path = '/home';
        navigate(path);
    };

    const toggleForm = () => {
        setShowSignUp(!showSignUp);
    };

    return (
        <div className="h-screen w-screen p-4 flex justify-center items-center custom-background">
        
            <div className="bg-white rounded-2xl w-1/2 shadow-2xl flex h-1/2">

                {showSignUp ? (
                    <div id="signUp" className='flex flex-col items-center justify-center space-y-5 p-10 w-1/2'>
                        <div>
                            <p className="text-3xl text-indigo-900 font-bold">SIGN UP</p> 
                        </div>
                        <div className="space-y-2 w-full">
                            <Input placeholder={"First Name"}></Input>
                            <Input placeholder={"Last Name"}></Input>
                            <Input placeholder={"Username"}></Input>
                            <Input placeholder={"Password"}></Input>
                        </div>
                        <div className="space-y-2 w-full">
                            <Button click={toggleForm} text={"Sign Up"} width={"100%"}></Button>
                            <div className="text-xs font-semibold flex space-x-1">
                                <p className="">Already a member?</p><button onClick={toggleForm} className="text-indigo-900">Log In</button>
                            </div>
                        </div>
                    </div>
                ) : (
                    <div id="logIn" className='flex flex-col items-center justify-center space-y-5 p-10 w-1/2'>
                        <div>
                            <p className="text-3xl text-indigo-900 font-bold">LOG IN</p> 
                        </div>
                        <div className="space-y-2 w-full">
                            <Input placeholder={"Username"}></Input>
                            <Input placeholder={"Password"}></Input>
                        </div>
                        <div className="space-y-2 w-full">
                            <Button click={homeRoute} text={"Login"} width={"100%"}></Button>
                            <div className="text-xs font-semibold flex space-x-1">
                                <p className="">Not a member?</p><button onClick={toggleForm} className="text-indigo-900">Sign Up</button>
                            </div>
                        </div>
                    </div>
                )}
                
                <div className='bg-indigo-900 w-1/2 rounded-2xl flex items-center justify-center'>
                    <img src={Logo} className="filter brightness-0 invert h-70" alt="Logo"></img>
                </div>

            </div>
        </div>
    )
}

export default Login;