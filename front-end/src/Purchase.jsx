import "./styles.css"
import { Navigate, useNavigate } from "react-router-dom";
import { useLocation } from "react-router-dom";
import axios from 'axios'
import { BASE_URL } from './config';

const Purchase = () => {

    const location = useLocation()
    const username = location.state.username
    const user_id = location.state.userId
    const order_id = location.state.order_id
    
    let navigate = useNavigate();
    const successRoute = () => {
        let path = '/orders';
        navigate(path, {state:{username: username, user_id: user_id}})
    }
    const failRoute = () => {
        let path = '/home';
        navigate(path, {state:{username}})
    }
    
    const success = async () => {
        try {
            const res = axios.put(`${BASE_URL}/api/v1/users/orders`, {
                user_id: user_id,
                order_id: order_id,
                order_status: 2
            })
            successRoute()
        } catch(error) {
        }
    }

    const fail = async () => {
        try {
            const res = await axios.put(`${BASE_URL}/api/v1/users/orders`, {
                user_id: user_id,
                order_id: order_id,
                order_status: 4

            })
            failRoute()
        } catch(error) {
        }
    }

    return (
        <div>
            <div className="custom-background p-4 h-screen flex justify-center items-center">
                <div className="bg-white rounded-2xl p-10 flex-col space-y-10 shadow-xl">
                    <div id="heading">
                        <p className="text-3xl text-indigo-900 font-bold">Confirm Your Purchase</p> 
                    </div>

                    <div id="buttons" className="flex justify-center space-x-4">
                        <button onClick={() => success()} className="btn btn-sm rounded-lg bg-green-600 p-2 content-center w-1/4">
                            <p className="text-white font-bold">
                                Success
                            </p>
                        </button> 
                        <button onClick={() => fail()} className="btn btn-sm rounded-lg bg-red-600 p-2 content-center w-1/4">
                            <p className="text-white font-bold">
                                Fail
                            </p>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Purchase;
