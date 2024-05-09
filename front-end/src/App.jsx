import "./index.css"
import { Route, Routes } from "react-router-dom"
import Home from "./Home.jsx"
import Login from "./Login.jsx"
import { ShopContextProvider } from "./context/ShopContext.jsx"

function App() {

  return (
    <div>
      <ShopContextProvider>
        <Routes>
          <Route path="/" element={<Login></Login>}></Route>
          <Route path="/home" element={<Home></Home>}></Route>
        </Routes>
      </ShopContextProvider>
    </div>
  )
}

export default App
