import "./styles.css"
import AdminOrder from "./components/AdminOrder";

const Admin = () => {

    return (
        <div className="custom-background p-4 h-screen">
            <div className="flex flex-col space-y-4 pt-4 pb-4 pr-10 pl-10">
                <AdminOrder orderId={"12313423"}></AdminOrder>
            </div>
        </div>
    )
}

export default Admin;