import { useState } from "react";
import CartItem from "./CartItem.jsx";
import { PRODUCTS } from "../products.js";
import {ShopContext} from "../context/ShopContext.jsx"
import {useContext} from "react"

const Cart = ({cart, setCart}) => {
    const {cartItems, removeFromCart, getTotal} = useContext(ShopContext)
    
    const totalPrice = getTotal()
    console.log(totalPrice);
    return (
        <div className="flex-col space-y-0.5">

            <div className="bg-white shadow-sm p-3 rounded-lg ">
                <p className="text-lg font-medium">Cart</p>
            </div>
            <div className="flex-row space-y-0.5 mr-2">
                {
                    PRODUCTS.map((product) => {
                        if (cartItems[product.id] != 0) {
                            return <CartItem handleClick={() => removeFromCart(product.id)} amount={cartItems[product.id]} type={product.type} price={product.price}></CartItem>
                        }
                    })
                }
            </div>

            <div className="flex-row space-y-2 mr-2 bg-white shadow-sm p-3 rounded-md">
                <div className="flex p-1 pl-3 pr-3 justify-between">
                    <p className="text-sm">Order Total: </p>
                    <p className="text-sm font-semibold">${totalPrice}</p>
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