import { observer } from "mobx-react-lite";
import { Formik, Form, Field } from "formik";
import authStore from "../store/authStore";
import { Link } from "react-router-dom";
import { useState } from "react";
import userService from "../serives/userService";

const ProfilePage = observer(() => {
  const user = authStore.user;
  const [status, setStatus] = useState("");
  
  if (authStore.isLoading) {
    return (
      <div className="flex justify-center items-center h-[60vh]">
        <div className="text-lg text-gray-600">Загрузка профиля...</div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto px-6 py-10 bg-white shadow-md rounded-xl">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold text-gray-800">Мой профиль</h2>
        {user.role === "admin" && (
          <Link
            to="/admin"
            className="bg-red-600 text-white px-4 py-2 rounded-full hover:bg-red-700 transition text-sm ml-12"
          >
            Админка
          </Link>
        )}
      </div>

      <Formik
        initialValues={{
          email: user.email || "",
          phone: user.phone || "",
          full_name: user.full_name || "",
        }}
        onSubmit={async (values, { setSubmitting }) => {
          setSubmitting(true);
          setStatus("");

          try {
            await userService.updateProfile(values);
            setStatus("Профиль обновлён");
            await authStore.setUser(); // Обновим локальные данные
          } catch (error) {
            setStatus("Ошибка при обновлении профиля");
            console.error(error);
          }

          setSubmitting(false);
        }}
      >
        {({ isSubmitting }) => (
          <Form className="space-y-6">
            <div>
              <label className="block text-lg font-medium text-gray-700 mb-1">Email</label>
              <Field
                type="email"
                name="email"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-100"
                disabled
              />
            </div>

            <div>
              <label className="block text-lg font-medium text-gray-700 mb-1">Телефон</label>
              <Field
                type="text"
                name="phone"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg"
              />
            </div>

            <div>
              <label className="block text-lg font-medium text-gray-700 mb-1">ФИО</label>
              <Field
                type="text"
                name="full_name"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg"
              />
            </div>

            <div>
              <label className="block text-lg font-medium text-gray-700 mb-1">Баланс</label>
              <div className="w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-50 text-gray-800">
                {user.balance} ₽
              </div>
            </div>

            {user.role === "admin" && (
              <div>
                <label className="block text-lg font-medium text-gray-700 mb-1">Роль</label>
                <div className="w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-100">
                  Администратор
                </div>
              </div>
            )}

            {status && (
              <div className="text-sm text-center text-green-600 font-medium">
                {status}
              </div>
            )}

            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full bg-red-600 text-white text-lg font-semibold py-3 rounded-lg hover:bg-red-700 transition"
            >
              {isSubmitting ? "Сохранение..." : "Сохранить изменения"}
            </button>
          </Form>
        )}
      </Formik>
    </div>
  );
});

export default ProfilePage;
