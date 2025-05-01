import { Route, Routes } from "react-router-dom"
import Layout from "./components/Layout"
import MainPage from "./pages/MainPage"
import SearchPage from "./pages/SearchPage"
import LoginPage from "./pages/LoginPage"

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout/>}>
        <Route index element={<MainPage/>} />
        <Route path="/s" element={<SearchPage/>}/>
        <Route path="/login" element={<LoginPage/>} />
      </Route>
    </Routes>
  )
}

export default App
