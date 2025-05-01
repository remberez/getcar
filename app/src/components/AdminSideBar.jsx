import { NavLink } from "react-router-dom";

const AdminSidebar = () => {
  const links = [
    { path: "/admin/cars", label: "Автомобили" },
    { path: "/admin/users", label: "Пользователи" },
  ];

  return (
    <aside className="w-64 bg-gray-100 p-4 shadow-inner">
      <h2 className="text-lg font-bold mb-4">Админ-панель</h2>
      <nav className="space-y-2">
        {links.map(link => (
          <NavLink
            key={link.path}
            to={link.path}
            className={({ isActive }) =>
              `block px-4 py-2 rounded hover:bg-gray-200 ${isActive ? "bg-gray-300 font-semibold" : ""}`
            }
          >
            {link.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
};

export default AdminSidebar;
