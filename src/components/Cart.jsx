import { useState } from "react";
import CartItem from "./CartItem";

const Cart = ({cart, setCart}) => {
    const [price, setPrice] = useState(0)

    return (
        <div className="flex-col space-y-0.5">
            <div className="bg-white shadow-sm p-3 rounded-lg ">
                <p className="text-lg font-medium">Cart</p>
            </div>
            <div>
            </div>
            <CartItem name={"Iced Latte"} price={"$7.50"}></CartItem>
            <div className="flex-row space-y-2 bg-white shadow-sm p-3 rounded-md">
                <div className="flex p-1 pl-3 pr-3 justify-between">
                    <p className="text-sm">Order Total:</p>
                    <p className="text-sm font-semibold">${price}</p>
                </div>
                <button className="btn btn-sm rounded-md bg-indigo-900 p-2 content-center w-full">
                    <p className="text-white">
                        Checkout
                    </p>
                </button> 
            </div>
        </div>
    )
}

export default Cart;