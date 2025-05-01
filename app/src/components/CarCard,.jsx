import React from 'react';

const CarCard = ({ car }) => {
  const year = new Date(car.year_of_issue).getFullYear();
  
  const formatPrice = (price) => {
    return new Intl.NumberFormat('ru-RU', {
      style: 'decimal',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(parseFloat(price));
  };

  const basePrice = parseFloat(car.price);
  const price4Days = basePrice * 0.96;
  const price11Days = basePrice * 0.92;
  const price21Days = basePrice * 0.88;

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <div className="bg-gray-100 p-6">
        <h1 className="text-3xl font-bold text-gray-800">
          Аренда {car.car_brand.name} {car.model} в Саратове
        </h1>
        <p className="mt-2 text-gray-600">
          Прокат {car.car_brand.name} {car.model} возможен на сутки и с правом выкупа. Прокат авто в Саратове без водителя или с водителем. Арендуйте {car.car_brand.name} {car.model} на свадьбу, личных или рабочих поездок.
        </p>
      </div>

      <div className="p-6 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-2">
          {car.images && car.images.length > 0 && (
            <img 
              src={"http://localhost:8000" + car.images[0].image_url} 
              alt={`${car.car_brand.name} ${car.model}`}
              className="w-full h-[400px] object-cover rounded-lg"
            />
          )}
          
          <div className="mt-4 flex flex-wrap gap-4">
            <div className="bg-blue-100 px-4 py-2 rounded-full">
              <span className="font-medium">{car.transmission.name} коробка передач</span>
            </div>
            <div className="bg-blue-100 px-4 py-2 rounded-full">
              <span className="font-medium">{car.engine_type.name} двигатель</span>
            </div>
            <div className="bg-blue-100 px-4 py-2 rounded-full">
              <span className="font-medium">{car.number_of_seats} мест</span>
            </div>
            <div className="bg-blue-100 px-4 py-2 rounded-full">
              <span className="font-medium">{car.trunk_volume} л багажник</span>
            </div>
            <div className="bg-blue-100 px-4 py-2 rounded-full">
              <span className="font-medium">{car.drive.name} привод</span>
            </div>
          </div>
        </div>

        <div className="bg-gray-50 p-6 rounded-lg">
          <h2 className="text-xl font-bold text-gray-800 mb-4">
            СТОИМОСТЬ ПРОКАТА {car.car_brand.name.toUpperCase()} {car.model.toUpperCase()} В САРАТОВЕ
          </h2>
          
          <div className="space-y-3 mb-6">
            <div className="flex justify-between">
              <span>от 0 суток:</span>
              <span className="font-bold">{formatPrice(basePrice)} руб.</span>
            </div>
            <div className="flex justify-between">
              <span>от 4 суток:</span>
              <span className="font-bold">{formatPrice(price4Days)} руб.</span>
            </div>
            <div className="flex justify-between">
              <span>от 11 суток:</span>
              <span className="font-bold">{formatPrice(price11Days)} руб.</span>
            </div>
            <div className="flex justify-between">
              <span>от 21 суток:</span>
              <span className="font-bold">{formatPrice(price21Days)} руб.</span>
            </div>
          </div>

          <p className="text-sm text-gray-600 mb-6">
            Чем больше срок аренды авто, тем ниже стоимость аренды за сутки
          </p>

          <button className="w-full bg-red-600 hover:bg-red-700 text-white font-bold py-3 px-4 rounded-lg transition duration-200">
            АРЕНДОВАТЬ
          </button>
        </div>
      </div>

      <div className="bg-gray-50 px-6 py-4 border-t border-gray-200">
        <div className="flex flex-wrap justify-between text-sm text-gray-600">
          <div className="mb-2">
            <span className="font-medium">Год выпуска:</span> {year}
          </div>
          <div className="mb-2">
            <span className="font-medium">Пробег:</span> {car.mileage.toLocaleString('ru-RU')} км
          </div>
          <div className="mb-2">
            <span className="font-medium">Класс:</span> {car.rental_class.name}
          </div>
          <div className="mb-2">
            <span className="font-medium">Кузов:</span> {car.body.name}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CarCard;