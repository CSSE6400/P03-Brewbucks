import Menu from "./components/Menu";
import Cart from "./components/Cart";

const Home = () => {
    return (
        <div className="bg-gray-100 p-4 h-dvh">
            <div className="flex space-x-8 pt-4 pb-4 pr-10 pl-10">
                <div className="w-3/4">
                    <Menu></Menu>
                </div>
                <div div className="w-1/4">
                    <Cart></Cart>
                </div>
            </div>
        </div>
    )
}

export default Home;