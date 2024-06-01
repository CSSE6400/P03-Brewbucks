import Coffee from "./components/Coffee.jsx"
import Store from "./components/Store.jsx"
import CartItem from "./components/CartItem.jsx";
import Navbar from "./components/Navbar";
import './styles.css';
import { useState, useEffect } from 'react'
import { useLocation } from "react-router-dom";
import { Navigate, useNavigate } from "react-router-dom";
import axios from 'axios'
import { BASE_URL } from './config';

const Home = () => {
    const [menu, setMenu] = useState([])
    const [userId, setUserId] = useState()

    const [addedProducts, setAddedProducts] = useState([]);
    const [orderTotal, setOrderTotal] = useState(0);

    const location = useLocation()
    const username = location.state.username

    const addProduct = (product) => {
        setAddedProducts(prevProducts => {
            const existingProduct = prevProducts.find(item => item.item_id === product.item_id);
            if (existingProduct) {
                return prevProducts.map(item =>
                    item.item_id === product.item_id
                        ? { ...item, quantity: item.quantity + 1 }
                        : item
                );
            } else {
                return [...prevProducts, { ...product, quantity: 1 }];
            }
        });
    };

    const removeProduct = (product) => {
        setAddedProducts(prevProducts => {
            const existingProduct = prevProducts.find(item => item.item_id === product.item_id);
            if (existingProduct.quantity === 1) {
                return prevProducts.filter(item => item.item_id !== product.item_id);
            } else {
                return prevProducts.map(item =>
                    item.item_id === product.item_id
                        ? { ...item, quantity: item.quantity - 1 }
                        : item
                );
            }
        });
    };
    
    let navigate = useNavigate();
    const paymentRoute= () => {
        let path = '/purchase';
        navigate(path, {state:{username}})
    }

    useEffect(() => {

        const fetchUserId = async () => {
            try {
                const res = await axios.post(`${BASE_URL}/api/v1/users/user_id`, {
                username: username,
            });
            setUserId(res.data.user_id)
            } catch (error) {
            }
        }

        const fetchMenu = async () => {
            try {
                const res = await axios.get(`${BASE_URL}/api/v1/menu_items`)
                setMenu(res.data)
            } catch (error) {
            }
        }

        fetchUserId();
        fetchMenu();
    }, [username]);

    useEffect(() => {
        const total = addedProducts.reduce((sum, product) => sum + product.price * product.quantity, 0);
        setOrderTotal(total);
    }, [addedProducts]);

    console.log(addedProducts)

    return (
        <div className="custom-background">
            <Navbar user={username}></Navbar>
            <div className="p-4">
                <div className="flex space-x-8 pt-4 pb-4 pr-10 pl-10">
                    <div className="w-3/4">
                        <div className="flex-col space-y-3">
                            <Store></Store>
                            <div className="flex-col space-y-1.5">
                                {
                                    menu.map((product) => {
                                        return <Coffee type={product.name} desc={product.description} price={product.price} handleClick={() => addProduct(product)}></Coffee>;
                                    })
                                }
                            </div>
                        </div>
                    </div>
                    <div div className="w-1/4">
                        <div className="flex-col space-y-0.5">
                            <div className="bg-white shadow-sm p-3 rounded-lg ">
                                <p className="text-lg font-medium">Cart</p>
                            </div>
                            <div className="flex-row space-y-0.5 mr-2">
                                {
                                    addedProducts.map((product) => {
                                            return <CartItem amount={product.quantity} handleClick={() => removeProduct(product)} type={product.name} price={(product.price * product.quantity).toFixed(2)}></CartItem>
                                        }
                                    )
                                }
                            </div>
                            <div className="flex-row space-y-2 mr-2 bg-white shadow-sm p-3 rounded-md">
                                <div className="flex p-1 pl-3 pr-3 justify-between">
                                    <p className="text-sm">Order Total: </p>
                                    <p className="text-sm font-semibold">${orderTotal.toFixed(2)}</p>
                                </div>
                                <button className="btn btn-sm rounded-md bg-indigo-900 p-2 content-center w-full" onClick={paymentRoute}>
                                    <p className="text-white">
                                        Checkout
                                    </p>
                                </button> 
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Home;