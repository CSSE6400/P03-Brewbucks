import Coffee from "./Coffee.jsx"
import Store from "./Store.jsx"
import {ShopContext} from "../context/ShopContext.jsx"
import {useContext} from "react"

const Menu = ({data}) => {
    
    const {addToCart} = useContext(ShopContext)

    return (
        <div className="flex-col space-y-3">
            <Store></Store>
            <div className="flex-col space-y-1.5">
                {
                    data.map((product) => {
                        return <Coffee type={product.name} desc={product.description} price={product.price} handleClick={() => addToCart(product.id)}></Coffee>;
                    })
                }
            </div>
        </div>
    )
}

export default Menu;