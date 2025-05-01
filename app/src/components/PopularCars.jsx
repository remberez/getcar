import { useEffect, useState } from "react";
import carService from "../serives/cars";
import { API_BASE_URL } from "../serives";

export default function PopularCars() {
    // const cars = [
    //   {
    //     name: "Аренда KIA Rio в Саратове",
    //     image: "/cars/kia.png",
    //     seats: 5,
    //     volume: "480 л.",
    //     transmission: "Автоматическая",
    //     fuel: "Бензин",
    //     price: "от 2700 руб. сутки",
    //   },
    //   {
    //     name: "Аренда Hyundai Solaris в Саратове",
    //     image: "/cars/solaris.png",
    //     seats: 5,
    //     volume: "480 л.",
    //     transmission: "Автоматическая",
    //     fuel: "Бензин",
    //     price: "от 2700 руб. сутки",
    //   },
    //   {
    //     name: "Аренда Toyota Camry в Саратове",
    //     image: "/cars/camry.png",
    //     seats: 5,
    //     volume: "480 л.",
    //     transmission: "Автоматическая",
    //     fuel: "Бензин",
    //     price: "от 6600 руб. сутки",
    //   },
    // ];

    const [cars, setCars] = useState([]);

    useEffect(() => {
      async function fetchData() {
        const data = await carService.getAllCars({offset: 0, limit: 3});
        setCars(data);
      }
      fetchData();
    }, [])
  
    return (
      <div className="py-10 container">
        <h2 className="text-2xl md:text-3xl font-bold uppercase mb-6">Популярные авто</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {cars?.map((car, index) => (
            <div key={index} className="border rounded-lg shadow-sm p-5 flex flex-col items-start bg-white">
              <img src={"http://localhost:8000" + car.images?.at(0)?.image_url} alt="" className="w-full h-50 object-cover mb-4 rounded-lg" />
              <h3 className="text-lg font-semibold mb-3">Аренда {car.car_brand?.name} {car.model}</h3>
              <div className="text-sm text-gray-700 space-y-1 mb-3">
                <div className="flex items-center gap-2"><span>👥Количество мест - </span>{car.number_of_seats}</div>
                <div className="flex items-center gap-2"><span>📦Вместительность багажника - </span>{car.trunk_volume} литров</div>
                <div className="flex items-center gap-2"><span>⚙️Коробка передач - </span>{car?.transmission?.name}</div>
                <div className="flex items-center gap-2"><span>⛽Тип двигателя - </span>{car.engine_type?.name}</div>
              </div>
              <p className="text-sm mb-2">Стоимость проката в Саратове <b>{car.price}</b></p>
              <p className="text-xs text-gray-500 mb-4">Чем больше срок аренды авто, тем ниже стоимость аренды за сутки</p>
              <button className="mt-auto border border-red-600 text-red-600 px-4 py-2 rounded-full hover:bg-red-600 hover:text-white transition">
                Арендовать
              </button>
            </div>
          ))}
        </div>
        <div className="mt-8 text-center">
          <button className="bg-red-600 text-white px-6 py-2 rounded-full hover:bg-red-700 transition">
            Посмотреть весь автопарк
          </button>
        </div>
      </div>
    );
}
  