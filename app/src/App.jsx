import { Route, Routes } from "react-router-dom"
import Layout from "./components/Layout"
import MainPage from "./pages/MainPage"
import SearchPage from "./pages/SearchPage"
import LoginPage from "./pages/LoginPage"
import ProfilePage from "./pages/ProfilePage"
import TopUpPage from "./pages/ToUpPage"
import AdminLayout from "./components/AdminLayout"
import CarsAdmin from "./pages/CarsAdmin"

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout/>}>
        <Route index element={<MainPage/>} />
        <Route path="/s" element={<SearchPage/>}/>
        <Route path="/login" element={<LoginPage/>} />
        <Route path="/profile" element={<ProfilePage/>}/>
        <Route path="/update-balance" element={<TopUpPage/>}/>
        <Route path="/admin" element={<AdminLayout />}>
          <Route path="cars" element={<CarsAdmin />} />
          {/* <Route path="users" element={<UsersAdmin />} /> */}
        </Route>
      </Route>
    </Routes>
  )
}

export default App
