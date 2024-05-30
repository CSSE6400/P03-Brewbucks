import OrderDetails from "./components/OrderDetails";
import Navbar from "./components/Navbar";
import "./styles.css"
import { useLocation } from "react-router-dom";
import { useState, useEffect } from 'react'
import axios from 'axios'

const Orders = () => {
    const [userId, setUserId] = useState()

    const location = useLocation()
    const username = location.state.username

    useEffect(() => {

        const fetchUserId = async () => {
            try {
                const res = await axios.post("http://127.0.0.1:8080/api/v1/users/user_id", {
                username: username,
            });
            setUserId(res.data.user_id)
            } catch (error) {
            }
        }

        fetchUserId();
    }, []);

    return (
        <div>
            <Navbar user={username}></Navbar>
            <div className="custom-background p-4 h-screen">
                <div className="flex flex-col space-y-4 pt-4 pb-4 pr-10 pl-10">
                    
                        <div tabIndex={0} className="collapse collapse-arrow bg-white shadow-sm p-2 rounded-lg w-full">
                            <div className="collapse-title text-xl font-medium">
                                Active Orders
                            </div>
                            <div className="collapse-content space-y-1"> 
                                <OrderDetails orderId={"12343134"} orderTime={"14:34, 18/05/2025"} orderPrice={"$15"} orderInfo={"1 Latte, 1 Mocha"} orderStatus={"Order Recieved"}></OrderDetails>
                                <OrderDetails orderTime={"14:34, 18/05/2025"} orderPrice={"$15"} orderInfo={"1 Latte, 1 Mocha"} orderStatus={"Order Recieved"}></OrderDetails>
                            </div>
                        </div>

                        <div tabIndex={0} className="collapse collapse-arrow bg-white shadow-sm p-2 rounded-lg w-full">
                            <div className="collapse-title text-xl font-medium">
                                Past Orders
                            </div>
                            <div className="collapse-content"> 
                                <OrderDetails orderTime={"12:30, 17/05/2025"} orderPrice={"$7.40"} orderInfo={"1 Latte"} orderStatus={"Finished"}></OrderDetails>
                            </div>
                        </div>

                </div>
            </div>
        </div>
    )
}

export default Orders;