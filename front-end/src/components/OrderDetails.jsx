const OrderDetails = ({orderTime, orderPrice, orderInfo, orderStatus}) => {
    return (
        <div className="p-4 shadow-sm rounded-xl">
            <div className="flex-col space-y-2">
                <div className="flex flex-row justify-between items-center">
                    <div className="flex flex-col space-y-1">
                        <p className="text-sm font-semibold">{orderTime}</p>
                        <p className="text-sm">{orderPrice}</p>
                        <p className="text-xs">{orderInfo}</p>
                    </div>
                    <div className="bg-gray-100 p-3 rounded-lg h-1/2">
                        <p className="text-lg font-semibold">{orderStatus}</p>
                    </div>
                </div>
            </div>
        </div>
    )
}
export default OrderDetails;