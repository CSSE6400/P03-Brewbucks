const Cart = () => {
    return (
        <div className="flex-col space-y-0.5">
            <div className="bg-white shadow-sm p-3 rounded-lg ">
                <p className="text-lg font-medium">Cart</p>
            </div>
            <div className="bg-white shadow-sm p-3 rounded-md">
                <p className="text-sm">Nothing in cart</p>
            </div>
            <div className="bg-white shadow-sm p-3 rounded-md">
                <button className="btn btn-sm rounded-md bg-indigo-900 p-2 content-center w-full">
                    <p className="text-white">
                        Checkout
                    </p>
                </button> 
            </div>
        </div>
    )
}

export default Cart;