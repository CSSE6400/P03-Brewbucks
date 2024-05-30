import Menu from "./components/Menu";
import Cart from "./components/Cart";
import Navbar from "./components/Navbar";
import './styles.css';
import { useState } from 'react'
import { useLocation } from "react-router-dom";

const Home = (props) => {
    const [menu, setMenu] = useState()

    const location = useLocation()
    const user = location.state.username

    return (
        <div>
            <Navbar user={user} ></Navbar>
            <div className="p-4 h-wscreen custom-background">
                <div className="flex space-x-8 pt-4 pb-4 pr-10 pl-10">
                    <div className="w-3/4">
                        <Menu></Menu>
                    </div>
                    <div div className="w-1/4">
                        <Cart></Cart>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Home;