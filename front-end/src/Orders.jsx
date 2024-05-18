import OrderDetails from "./components/OrderDetails";
import Navbar from "./components/Navbar";
import { useState } from "react";

const Orders = () => {
    return (
        <div>
            <Navbar></Navbar>
            <div className="bg-gray-100 p-4 h-dvh">
                <div className="flex flex-col space-y-4 pt-4 pb-4 pr-10 pl-10">
                    
                        <div tabIndex={0} className="collapse collapse-arrow bg-white shadow-sm p-2 rounded-lg w-full">
                            <div className="collapse-title text-xl font-medium">
                                Active Orders
                            </div>
                            <div className="collapse-content"> 
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