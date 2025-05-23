import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { observer } from "mobx-react-lite";
import authStore from "../store/authStore";

const Header = () => {
  const [isProfileOpen, setIsProfileOpen] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      authStore.setToken(token);
      authStore.setUser();
    }
  }, []);

  return (
    <header className="bg-[#F5F5F5] border-b border-[#E0E0E0]">
      <div className="container flex justify-between items-center py-4">
        <div className="flex items-center gap-4">
          <h1 className="text-2xl font-bold text-[#333333]">
            <Link to={"/"}>
              GetCar
            </Link>
          </h1>
          <div className="text-[#666666] text-sm">
            <div className="flex gap-2">
              <span>+7 917 100-00-50</span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-6">
          <div className="text-right">
            <div className="font-medium text-[#333333]">Саратов</div>
            <div className="text-[#666666] text-sm">
              Ежеденевно с 9:00 до 21:00
            </div>
          </div>

          <div className="relative">
            {authStore.isAuth ? (
              <>
                <button
                  onClick={() => setIsProfileOpen(!isProfileOpen)}
                  className="bg-[#E0E0E0] hover:bg-[#D0D0D0] text-[#333333] px-4 py-2 rounded-md text-sm transition-colors"
                >
                  Профиль
                </button>

                {isProfileOpen && (
                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg border border-[#E0E0E0] z-10">
                    <Link
                      to={"/profile"}
                      className="block px-4 py-2 text-sm text-[#333333] hover:bg-[#F5F5F5]"
                    >
                      Мой профиль
                    </Link>
                    <Link
                      to={"/my-bookings"}
                      className="block px-4 py-2 text-sm text-[#333333] hover:bg-[#F5F5F5]"
                    >
                      Мои бронирования
                    </Link>
                    <button
                      onClick={() => {
                        authStore.setToken(null);
                        authStore.setUser(); // сбросит user
                      }}
                      className="w-full text-left px-4 py-2 text-sm text-[#333333] hover:bg-[#F5F5F5] border-t border-[#E0E0E0]"
                    >
                      Выйти
                    </button>
                  </div>
                )}
              </>
            ) : (
              <Link
                to="/login"
                className="bg-[#E0E0E0] hover:bg-[#D0D0D0] text-[#333333] px-4 py-2 rounded-md text-sm transition-colors"
              >
                Войти
              </Link>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default observer(Header);
