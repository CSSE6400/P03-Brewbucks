import "./index.css"
import { Route, Routes } from "react-router-dom"
import Home from "./Home.jsx"

function App() {

  return (
    <div>
      <div className="bg-white p-4">
        <h1 className="text-3xl text-indigo-900 font-bold">Brewbucks</h1>
      </div>
    
      <Routes>
        <Route path="/" element={<Home></Home>}></Route>
      </Routes>
    </div>
  )
}

export default App
