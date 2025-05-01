import { useEffect, useState } from "react";
import { Formik, Form, Field } from "formik";
import carService from "../serives/cars";

const CarsPage = () => {
  const [cars, setCars] = useState([]);

  useEffect(() => {
    const fetchCars = async () => {
      const data = await carService.getAllCars({});
      setCars(data);
    };
    fetchCars();
  }, []);

  return (
    <div className="p-6 space-y-10">
      <div className="bg-white p-6 rounded-xl shadow">
        <h2 className="text-xl font-bold mb-4">Добавить автомобиль</h2>
        <Formik
          initialValues={{
            car_brand_id: "",
            model: "",
            transmission_id: "",
            body_id: "",
            year_of_issue: "",
            engine_type_id: "",
            drive_id: "",
            mileage: "",
            price: "",
            rental_class_id: "",
            number_of_seats: "",
            trunk_volume: "",
          }}
          onSubmit={(values) => {
            console.log("submitted", values);
          }}
        >
          <Form className="grid grid-cols-3 gap-4">
            <Field name="car_brand_id" placeholder="Марка" className="form-input" />
            <Field name="model" placeholder="Модель" className="form-input" />
            <Field name="transmission_id" placeholder="Трансмиссия" className="form-input" />
            <Field name="body_id" placeholder="Кузов" className="form-input" />
            <Field name="year_of_issue" type="date" className="form-input" />
            <Field name="engine_type_id" placeholder="Тип двигателя" className="form-input" />
            <Field name="drive_id" placeholder="Привод" className="form-input" />
            <Field name="mileage" type="number" placeholder="Пробег" className="form-input" />
            <Field name="price" type="number" placeholder="Цена" className="form-input" />
            <Field name="rental_class_id" placeholder="Класс аренды" className="form-input" />
            <Field name="number_of_seats" type="number" placeholder="Кол-во мест" className="form-input" />
            <Field name="trunk_volume" type="number" placeholder="Объём багажника" className="form-input" />
            <button type="submit" className="col-span-3 bg-blue-600 text-white py-2 rounded">
              Добавить
            </button>
          </Form>
        </Formik>
      </div>

      <div className="bg-white p-6 rounded-xl shadow">
        <h2 className="text-xl font-bold mb-4">Список автомобилей</h2>
        <table className="table-auto border-separate border-spacing-y-4 w-full">
            <thead>
                <tr>
                <th>Модель</th>
                <th>Бренд</th>
                <th>Цена за час</th>
                <th>Год</th>
                </tr>
            </thead>
            <tbody>
                {cars.map((car) => (
                <tr key={car.id} className="bg-white shadow rounded-lg">
                    <td className="text-center">{car.model}</td>
                    <td className="text-center">{car.car_brand?.name}</td>
                    <td className="text-center">{car.price} ₽</td>
                    <td className="text-center">{new Date(car.year_of_issue).getFullYear()}</td>
                    <td className="text-center">
                        <button className="bg-red-600 text-white px-4 rounded-lg">Удалить</button>
                    </td>
                </tr>
                ))}
            </tbody>
        </table>
      </div>
    </div>
  );
};

export default CarsPage;