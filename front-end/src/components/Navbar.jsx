import AvatarMenu from "./AvatarMenu";

const Navbar = () => {
    return (
        <div className="bg-white p-4">
            <div className="flex items-center space-x-3 justify-between pl-8 pr-8">
                <p className="text-3xl text-indigo-900 font-bold">BREWBUCKS</p> 
                <AvatarMenu points={99999}></AvatarMenu>
            </div>
        </div>
    )
}

export default Navbar;