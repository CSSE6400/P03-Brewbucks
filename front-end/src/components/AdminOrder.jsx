import Button from "./Button";

const AdminOrder = ({orderId, orderStatus}) => {
    return (
        <div className="rounded-xl bg-gradient-to-tr from-pink-300 to-blue-300 p-0.5">
            <div className="p-4  bg-white shadow-sm rounded-xl">
                <div className="flex-col space-y-2">
                    <div className="flex flex-row justify-between items-center">
                        <div className="flex flex-col space-y-1">
                            <p className="text-sm font-semibold">Order ID: <span className="font-normal">{orderId}</span></p>
                        </div>
                        <div className="flex items-center space-x-1">
                            <p className="text-sm font-semibold">Update Status: </p>
                            <Button text={"Finished"}></Button>
                            <Button text={"Cancelled"}></Button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
export default AdminOrder;