import "./index.css"
import { Route, Routes } from "react-router-dom"
import Home from "./Home.jsx"
import { ShopContextProvider } from "./context/ShopContext.jsx"

function App() {

  return (
    <div>
      <ShopContextProvider>
        <Routes>
          <Route path="/" element={<Home></Home>}></Route>
        </Routes>
      </ShopContextProvider>
    </div>
  )
}

export default App
