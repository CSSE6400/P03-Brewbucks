import "./index.css"
import { Route, Routes } from "react-router-dom"
import Home from "./Home.jsx"
import Login from "./Login.jsx"
import { ShopContextProvider } from "./context/ShopContext.jsx"
import Purchase from "./Purchase.jsx"
import Orders from "./Orders.jsx"
import Admin from "./Admin.jsx"

function App() {

  return (
    <div>
      <ShopContextProvider>
        <Routes>
          <Route path="/" element={<Login></Login>}></Route>
          <Route path="/home" element={<Home></Home>}></Route>
          <Route path="/purchase" element={<Purchase></Purchase>}></Route>
          <Route path="/orders" element={<Orders></Orders>}></Route>
          <Route path="/admin" element={<Admin></Admin>}></Route>
        </Routes>
      </ShopContextProvider>
    </div>
  )
}

export default App
