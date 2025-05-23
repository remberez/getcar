import { useState } from "react";
import { useNavigate } from "react-router-dom";
import authService from "../serives/authService";

const RegisterPage = () => {
  const [form, setForm] = useState({
    email: "",
    password: "",
    phone: "",
    full_name: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await authService.register(form);
      navigate("/login");
    } catch (e) {
      setError(e?.response?.data?.detail || "Ошибка регистрации");
    }
    setLoading(false);
  };

  return (
    <div className="max-w-md mx-auto mt-12 bg-white p-8 rounded-xl shadow">
      <h2 className="text-2xl font-bold mb-6 text-center">Регистрация</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          className="w-full border rounded px-3 py-2"
          type="email"
          name="email"
          placeholder="E-mail"
          value={form.email}
          onChange={handleChange}
          required
        />
        <input
          className="w-full border rounded px-3 py-2"
          type="password"
          name="password"
          placeholder="Пароль"
          value={form.password}
          onChange={handleChange}
          required
        />
        <input
          className="w-full border rounded px-3 py-2"
          type="text"
          name="phone"
          placeholder="Телефон"
          value={form.phone}
          onChange={handleChange}
          required
        />
        <input
          className="w-full border rounded px-3 py-2"
          type="text"
          name="full_name"
          placeholder="ФИО"
          value={form.full_name}
          onChange={handleChange}
          required
        />
        {error && <div className="text-red-600">{error}</div>}
        <button
          type="submit"
          className="w-full bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
          disabled={loading}
        >
          {loading ? "Регистрация..." : "Зарегистрироваться"}
        </button>
      </form>
    </div>
  );
};

export default RegisterPage;