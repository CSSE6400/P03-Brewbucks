import "./index.css"
import { Route, Routes } from "react-router-dom"
import Home from "./Home.jsx"

function App() {

  return (
    <div>
      <Routes>
        <Route path="/" element={<Home></Home>}></Route>
      </Routes>
    </div>
  )
}

export default App
