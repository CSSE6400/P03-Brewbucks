import CartItem from "./CartItem.jsx";
import { Navigate, useNavigate } from "react-router-dom";


const Cart = ({products, remove}) => {
    
    console.log("cart")
    console.log(products)

    let navigate = useNavigate();
    const routeChange = () => {
        let path = '/purchase';
        navigate(path);
    }

    return (
        
        <div className="flex-col space-y-0.5">

            <div className="bg-white shadow-sm p-3 rounded-lg ">
                <p className="text-lg font-medium">Cart</p>
            </div>
            <div className="flex-row space-y-0.5 mr-2">
                {
                    products.map((product) => {
                            <CartItem type={"hello"} price={"prioe"}></CartItem>
                        }
                    )
                }
            </div>

            <div className="flex-row space-y-2 mr-2 bg-white shadow-sm p-3 rounded-md">
                <div className="flex p-1 pl-3 pr-3 justify-between">
                    <p className="text-sm">Order Total: </p>
                    <p className="text-sm font-semibold">Fetch Price Here</p>
                </div>
                <button className="btn btn-sm rounded-md bg-indigo-900 p-2 content-center w-full" onClick={routeChange}>
                    <p className="text-white">
                        Checkout
                    </p>
                </button> 
            </div>
            
        </div>
    )
}

export default Cart;