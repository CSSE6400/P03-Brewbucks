import { useState, useEffect } from 'react'
import AvatarMenu from "./AvatarMenu";
import { Navigate, useNavigate } from "react-router-dom";
import Button from "./Button";
import axios from 'axios'
import { BASE_URL } from '../config';

const Navbar = ({user, userId}) => {
    const [rewardPoints, setRewardPoints] = useState(0)

    let navigate = useNavigate();

    const username = user
    const user_id = userId

    const homeRoute = () => {
        let path = '/home';
        navigate(path, {state:{username: username}})
    }

    const ordersRoute = () => {
        let path = '/orders';
        navigate(path, {state:{username: username, user_id: user_id}});
    }

    useEffect(() => {

        const fetchRewardPoints = async () => {
            try {
                const res = await axios.get(`${BASE_URL}/api/v1/users/rewards`, {
                    params: { user_id }
                });
                setRewardPoints(res.data["User points"][0])
            } catch (error) {
            }
        }

        fetchRewardPoints();
    }, []);

    return (
        <div className="sticky top-0 z-50 shadow-md bg-white p-3">
            <div className="flex items-center space-x-3 justify-between pl-8 pr-8">
                <p className="text-3xl text-indigo-900 font-bold">BREWBUCKS</p> 
                <div className="flex space-x-8 items-center">
                    <div className="flex space-x-2">
                        <Button click={homeRoute} text={"Home"} width={"100%"}></Button>
                        <Button click={ordersRoute} text={"Orders"} width={"100%"}></Button>
                    </div>
                    <div className="flex items-center space-x-2">
                        <AvatarMenu username={username}points={rewardPoints}></AvatarMenu>
                        
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Navbar;