import Menu from "./components/Menu";
import Cart from "./components/Cart";
import Navbar from "./components/Navbar";
import './styles.css';
import { useState, useEffect } from 'react'
import { useLocation } from "react-router-dom";
import axios from 'axios'

const Home = () => {
    const [menu, setMenu] = useState([])
    const [error, setError] = useState(false)
    const [userId, setUserId] = useState()

    const location = useLocation()
    const username = location.state.username
    
    useEffect(() => {

        const fetchUserId = async () => {
            try {
                const res = await axios.post("http://127.0.0.1:8080/api/v1/users/user_id", {
                username: username,
            });
            setUserId(res.data.user_id)
            } catch (error) {
            }
        }

        const fetchMenu = async () => {
            try {
                const res = await axios.get('http://127.0.0.1:8080/api/v1/menu_items')
                setMenu(res.data)
            } catch (error) {
                setError(true)
            }
        }

        fetchUserId();
        fetchMenu();
    }, []);

    return (
        <div className="custom-background">
            <Navbar user={username} ></Navbar>
            <div className="p-4">
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