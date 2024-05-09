import Coffee from "./Coffee.jsx"
import Store from "./Store.jsx"
import {PRODUCTS} from "../products.js"
import {ShopContext} from "../context/ShopContext.jsx"
import {useContext} from "react"

const Menu = () => {
    
    const {addToCart} = useContext(ShopContext)

    return (
        <div className="flex-col space-y-3">
            <Store></Store>
            <div className="flex-col space-y-1.5">
                {
                    PRODUCTS.map((product) => {
                        return <Coffee type={product.type} desc={product.desc} price={product.price} handleClick={() => addToCart(product.id)}></Coffee>;
                    })
                }
            </div>
        </div>
    )
}

export default Menu;