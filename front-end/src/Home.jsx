import Menu from "./components/Menu";
import Cart from "./components/Cart";
import Navbar from "./components/Navbar";
import './styles.css';
import { useState, useEffect } from 'react'
import { useLocation } from "react-router-dom";
import axios from 'axios'

const Home = (props) => {
    const [menu, setMenu] = useState([])
    const [error, setError] = useState(false)
    const [userId, setUserId] = useState()

    const location = useLocation()
    const user = location.state.username
    
    useEffect(() => {
        const fetchMenu = async () => {
            try {
                const res = await axios.get('http://127.0.0.1:8080/api/v1/menu_items')
                setMenu(res.data)
            } catch (error) {
                setError(true)
            }
        }

        fetchMenu();
    }, []);

    return (
        <div>
            <Navbar user={user} ></Navbar>
            <div className="p-4 h-screen custom-background">
                <div className="flex space-x-8 pt-4 pb-4 pr-10 pl-10">
                    <div className="w-3/4">
                        <Menu data={menu}></Menu>
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