import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Button from "./components/Button";
import Input from "./components/Input";
import Logo from "./images/logo.png";
import './styles.css'
import axios from 'axios'
import { Link } from 'react-router-dom';

const Login = () => {
    const [showSignUp, setShowSignUp] = useState(false);
    const navigate = useNavigate();

    const [firstname, setFirstname] = useState("");
    const [lastname, setLastname] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(false)
    const [signUpError, setSignUpError] = useState(false)

    const homeRoute = () => {
        let path = '/home';
        navigate(path, {state:{username}})
    };

    const toggleForm = () => {
        setShowSignUp(!showSignUp);
    }

    const signup = async () => {
        try {
            const res = await axios.post("http://127.0.0.1:8080/api/v1/users", {
                first_name: firstname,
                last_name: lastname,
                username: username,
                password: password
            });
            toggleForm()
        } catch (error) {
            setSignUpError(true);
        }
    };

    const login = async () => {
        try {
            const res = await axios.post("http://127.0.0.1:8080/api/v1/users/login", {
                username: username,
                password: password
            });
            homeRoute();
        } catch (error) {
            setError(true);
        }
    }

    return (
        <div className="h-screen w-screen p-4 flex justify-center items-center custom-background">
        
            <div className="bg-white rounded-2xl w-1/2 shadow-2xl flex h-1/2">

                {showSignUp ? (
                    <div id="signUp" className='flex flex-col items-center justify-center space-y-5 p-10 w-1/2'>
                        <div>
                            <p className="text-3xl text-indigo-900 font-bold">SIGN UP</p> 
                        </div>
                        {
                            signUpError && <div className="text-xs text-red-500">
                                <p>Incorrect username or password</p>
                            </div>
                        }
                        <div className="space-y-2 w-full">
                            <input className="input input-bordered input-sm w-full max-w-md" placeholder={"First Name"} onChange={(e) => setFirstname(e.target.value)}></input>
                            <input className="input input-bordered input-sm w-full max-w-md" placeholder={"Last Name"} onChange={(e) => setLastname(e.target.value)}></input>
                            <input className="input input-bordered input-sm w-full max-w-md" placeholder={"Username"} onChange={(e) => setUsername(e.target.value)}></input>
                            <input className="input input-bordered input-sm w-full max-w-md" placeholder={"Password"} onChange={(e) => setPassword(e.target.value)}></input>
                        </div>
                        <div className="space-y-2 w-full">
                            <Button click={signup} text={"Sign Up"} width={"100%"}></Button>
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
                        {
                            error && <div className="text-xs text-red-500">
                                <p>Incorrect username or password</p>
                            </div>
                        }
                        <div className="space-y-2 w-full">
                            <input className="input input-bordered input-sm w-full max-w-md" placeholder={"Username"} onChange={(e) => setUsername(e.target.value)}></input>
                            <input className="input input-bordered input-sm w-full max-w-md" placeholder={"Password"} onChange={(e) => setPassword(e.target.value)}></input>
                        </div>
                        <div className="space-y-2 w-full">
                            <Button click={login} text={"Login"} width={"100%"}></Button>
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