import "./styles.css"
import axios from "axios";
import { BASE_URL } from './config';
import { useState, useEffect } from 'react'

const Admin = () => {
    const [makingOrders, setMakingOrders] = useState()


    const fetchOrders = async () => {
        try {
            const res = await axios.get(`${BASE_URL}/api/v1/orders/display_screen`)
            setMakingOrders(res.data)
        } catch (error) {
        }
    }

    const cancelled = async (user_id, order_id) => {
        try {
            const res = await axios.put(`${BASE_URL}/api/v1/users/orders`, {
                user_id: user_id,
                order_id: order_id,
                order_status: 4
            })
            console.log(res)
        } catch(error) {
        }
        fetchOrders()
    }

    const completed = async (user_id, order_id) => {
        try {
            const res = await axios.put(`${BASE_URL}/api/v1/users/orders`, {
                user_id: user_id,
                order_id: order_id,
                order_status: 3
            })
            console.log(res)
        } catch(error) {
        }
        fetchOrders()
    }

    
    useEffect(() => {
        fetchOrders()
    }, []);

    return (
        <div className="custom-background h-screen p-4 ">
            <div className="flex flex-col space-y-4 pt-4 pb-4 pr-10 pl-10">
                {
                    makingOrders && makingOrders.map((order) => {
                        return (
                            <div className="rounded-xl bg-gradient-to-tr from-pink-300 to-blue-300 p-0.5">
                                <div className="p-4  bg-white shadow-sm rounded-xl">
                                    <div className="flex-col space-y-2">
                                        <div className="flex flex-row justify-between items-center">
                                            <div className="flex flex-col space-y-1">
                                                <p className="text-sm font-semibold">Order ID: <span className="font-normal">{order.order_id}</span></p>
                                                <p className="text-sm font-semibold">Order Date: <span className="font-normal">{order.created_at}</span></p>
                                                <p className="text-sm font-semibold">Order Status: <span className="font-normal">{order.order_status}</span></p>
                                            </div>
                                            <div className="flex items-center space-x-1">
                                                <p className="text-sm font-semibold">Update Status: </p>
                                                <button className="btn btn-sm rounded-lg bg-indigo-900 p-2 content-center" onClick={() => completed(order.user_id, order.order_id)}>
                                                    <p className="text-white font-bold">
                                                        Completed
                                                    </p>
                                                </button>
                                                <button className="btn btn-sm rounded-lg bg-indigo-900 p-2 content-center" onClick={() => cancelled(order.user_id, order.order_id)}>
                                                    <p className="text-white font-bold">
                                                        Cancelled
                                                    </p>
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )
                    })
                }
            </div>
        </div>
    )
}

export default Admin;