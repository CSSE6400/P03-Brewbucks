const CartItem = ({name, price}) => {
    return (
        <div className="bg-white shadow-sm p-3 pl-6 pr-6 rounded-md flex justify-between">
            <p className="text-sm">{name}</p>
            <p className="text-sm font-medium">{price}</p>
        </div>
    )
}

export default CartItem;