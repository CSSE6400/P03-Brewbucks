import Menu from "./components/Menu";
import Cart from "./components/Cart";

const Home = () => {
    return (
        <div className="bg-gray-100 p-4 h-dvh">
            <div className="flex space-x-6 items-start justify-center">
                <Menu></Menu>
                <Cart></Cart>
            </div>
        </div>
    )
}

export default Home;