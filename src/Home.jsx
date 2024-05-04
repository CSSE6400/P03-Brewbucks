import Menu from "./components/Menu";
import Cart from "./components/Cart";
import { useState } from "react";

const Home = () => {

    const [cart, setCart] = useState(true);

    const handleClick = ({name, price}) => {
        console.log(name)
        console.log(price)
    }

    return (
        <div className="bg-gray-100 p-4 h-dvh">
            <div className="flex space-x-8 pt-4 pb-4 pr-10 pl-10">
                <div className="w-3/4">
                    <Menu handleClick={handleClick}></Menu>
                </div>
                <div div className="w-1/4">
                    <Cart cart={cart} setCart={cart}></Cart>
                </div>
            </div>
        </div>
    )
}

export default Home;