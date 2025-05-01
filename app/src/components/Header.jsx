import { useState } from "react";
import { Link } from "react-router-dom";

export const Header = () => {
  const [isProfileOpen, setIsProfileOpen] = useState(false);

  return (
    <header className="bg-[#F5F5F5] border-b border-[#E0E0E0]">
      <div className="container flex justify-between items-center py-4">
        <div className="flex items-center gap-4">
            <h1 className="text-2xl font-bold text-[#333333]">GetCar</h1>
            
            <div className="text-[#666666] text-sm">
            <div className="flex gap-2">
                <span>+7 917 100-00-50</span>
            </div>
            </div>
        </div>

        <div className="flex items-center gap-6">
            <div className="text-right">
            <div className="font-medium text-[#333333]">Саратов</div>
            <div className="text-[#666666] text-sm">Ежеденевно с 9:00 до 21:00</div>
            </div>

            <div className="relative">
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
                        to={"/settings"}
                        className="block px-4 py-2 text-sm text-[#333333] hover:bg-[#F5F5F5]"
                    >
                        Настройки
                    </Link>
                    <Link
                        to={"/exit"}
                        className="block px-4 py-2 text-sm text-[#333333] hover:bg-[#F5F5F5] border-t border-[#E0E0E0]"
                    >
                        Выйти
                    </Link>
                </div>
            )}
            </div>
        </div>
      </div>
    </header>
  );
};