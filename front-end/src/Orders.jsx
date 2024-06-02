import OrderDetails from "./components/OrderDetails";
import Navbar from "./components/Navbar";
import "./styles.css"
import { useLocation } from "react-router-dom";
import { useState, useEffect } from 'react'
import axios from 'axios'
import { BASE_URL } from "./config";


const Orders = () => {
    const [activeOrders, setActiveOrders] = useState()
    const [finishedOrders, setFinishedOrders] = useState()

    const location = useLocation()
    const username = location.state.username
    const user_id = location.state.user_id

    useEffect(() => {
        const fetchActiveOrders = async () => {
            console.log(user_id)
            try {
                const res = await axios.get(`${BASE_URL}/api/v1/orders/making`, { 
                    user_id: user_id,
                });
                console.log(res)
                setActiveOrders(res.data)
            } catch (error) {
                console.log(error)
            }
        }

        const fetchFinishedOrders = async () => {
            try {
                const res = await axios.get(`${BASE_URL}/api/v1/orders/finished`, {
                    user_id: user_id,
                });
                setFinishedOrders(res.data)
            } catch (error) {
            }
        }
        
        fetchActiveOrders();
        fetchFinishedOrders();
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