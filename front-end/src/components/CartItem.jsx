const CartItem = ({amount, type, price, handleClick}) => {
    return (
        <div className="bg-white shadow-sm p-3 pl-6 pr-6 rounded-md flex justify-between">
            <div className="flex items-center space-x-1.5">
                <button onClick={handleClick} className="btn btn-xs bg-indigo-900 p-1.5 content-center">
                    <p className="text-2xl text-white font-black pb-2">-</p>
                </button> 
                <p className="text-sm">{amount} x {type}</p>
            </div>
            <p className="text-sm font-medium"> ${price}</p>
        </div>
    )
}

export default CartItem;