import { useEffect, useState } from "react";
import rentalClass from "../serives/rentalClass";

export default function CarRentalForm() {
  const [carType, setCarType] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [rentalClasses, setRentalClasses] = useState([]);

  useEffect(() => {
    async function fetchData() {
        const data = await rentalClass.getList();
        setRentalClasses(data);
    }
    fetchData();
  }, []);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 p-6 bg-gray-50 min-h-[80vh] font-sans container py-20">
      <div className="space-y-6 self-center">
        <h1 className="text-3xl font-bold uppercase">
          Прокат и аренда авто в <span className="text-red-600">Саратове</span>
        </h1>

        <div className="bg-white rounded-xl shadow p-6 space-y-4">
          <div>
            <p className="font-semibold text-lg mb-2">A. Арендовать авто в Саратове</p>
            <select
              value={carType}
              onChange={(e) => setCarType(e.target.value)}
              className="w-full border rounded px-3 py-2"
            >
              {
                rentalClasses?.map(value => (
                    <option key={value.id}>
                        {value.name}
                    </option>
                ))
              }
            </select>
          </div>

          <div>
            <label className="block text-sm text-gray-600 mb-1">Дата начала аренды</label>
            <input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              className="w-full border rounded px-3 py-2"
            />
          </div>

          <div>
            <p className="font-semibold text-lg mb-2">B. Вернуть авто</p>
            <label className="block text-sm text-gray-600 mb-1">Дата конца аренды</label>
            <input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              className="w-full border rounded px-3 py-2"
            />
          </div>

          <div className="flex space-x-2 pt-2">
            <button className="border px-4 py-2 rounded hover:bg-gray-100">Аренда в 1 клик</button>
            <button className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700">
              Подобрать авто
            </button>
          </div>
        </div>
      </div>

      <div className="grid gap-6">
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-white rounded-xl shadow p-4 text-center">
            <p className="text-xl font-bold">Эконом</p>
            <p className="text-red-600 font-semibold">от 1800 ₽/сутки</p>
          </div>
          <div className="bg-white rounded-xl shadow p-4 text-center">
            <p className="text-xl font-bold">Комфорт</p>
            <p className="text-red-600 font-semibold">от 2100 ₽/сутки</p>
          </div>
        </div>
        <div className="bg-white rounded-xl shadow p-4 text-center">
          <p className="text-xl font-bold">Бизнес</p>
          <p className="text-red-600 font-semibold">от 6600 ₽/сутки</p>
        </div>
      </div>
    </div>
  );
}
