import { createContext } from "react"
import { PRODUCTS } from "../products";
import React from "react";
import { useState } from "react";

export const ShopContext = createContext(null);

const getDefaultCart = () => {
    let cart = {}
    for (let i = 1; i < PRODUCTS.length + 1; i++) {
        cart[i] = 0; 
    }
    return cart
}

export const ShopContextProvider = (props) => {
        const [cartItems, setCartItems] = useState(getDefaultCart())

        const getTotal = () => {
            let totalAmount = 0;
            for (const item in cartItems) {
                if (cartItems[item] > 0) {
                    let itemInfo = PRODUCTS.find((product) => product.id === Number(item));
                    totalAmount += cartItems[item] * itemInfo.price
                }
            }
            return totalAmount
        }

        const addToCart = (itemId) => {
            setCartItems((prev) => ({...prev, [itemId]: prev[itemId] + 1}))
        }

        const removeFromCart = (itemId) => {
            setCartItems((prev) => ({...prev, [itemId]: prev[itemId] - 1}))
        }

        const contextValue = {cartItems, addToCart, removeFromCart, getTotal}
    return (
        <ShopContext.Provider value={contextValue}>{props.children}</ShopContext.Provider>
    )
}