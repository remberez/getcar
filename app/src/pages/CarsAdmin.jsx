import { useEffect, useState } from "react";
import { Formik, Form, Field } from "formik";
import carService from "../serives/cars";
import { carBodyService, carBrandService, driveTypeService, engineTypeService, rentalClassService, transmissionService } from "../serives/vehicleСomponentsService";

const CarsPage = () => {
  const [cars, setCars] = useState([]);
  const [brands, setBrands] = useState([]);
  const [transmissions, setTransmissions] = useState([]);
  const [bodies, setBodies] = useState([]);
  const [engineTypes, setEngineTypes] = useState([]);
  const [driveTypes, setDriveTypes] = useState([]);
  const [rentalClasses, setRentalClasses] = useState([]);

  useEffect(() => {
    async function fetchOptions() {
      setBrands(await carBrandService.getAll());
      setTransmissions(await transmissionService.getAll());
      setBodies(await carBodyService.getAll());
      setEngineTypes(await engineTypeService.getAll());
      setDriveTypes(await driveTypeService.getAll());
      setRentalClasses(await rentalClassService.getAll());
    }
    const fetchCars = async () => {
      const data = await carService.getAllCars({});
      setCars(data);
    };
    fetchCars();
    fetchOptions();
  }, []);

  const onSubmitCreate = async (values) => {
    const carData = await carService.createCar({...values});
    
    if (carData) {
      setCars([...cars, carData]);
    }
  };

  async function onCarDelete(carId) {
    const response = await carService.deleteCar(carId);

    if (response.status === 204) {
        setCars((prevCars) => prevCars.filter(car => car.id !== carId));
    }
  }

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
          onSubmit={onSubmitCreate}
        >
          {({ setFieldValue }) => (
            <Form className="grid grid-cols-3 gap-4">
              <Field
                as="select"
                name="car_brand_id"
                className="form-input"
                onChange={e => {
                  const value = e.target.value ? parseInt(e.target.value, 10) : "";
                  setFieldValue('car_brand_id', value); // используем setFieldValue
                }}
              >
                <option value="">Выберите марку</option>
                {brands.map((b) => (
                  <option key={b.id} value={b.id}>{b.name}</option>
                ))}
              </Field>

              <Field name="model" placeholder="Модель" className="form-input" />

              <Field
                as="select"
                name="transmission_id"
                className="form-input"
                onChange={e => {
                  const value = e.target.value ? parseInt(e.target.value, 10) : "";
                  setFieldValue('transmission_id', value); // используем setFieldValue
                }}
              >
                <option value="">Выберите трансмиссию</option>
                {transmissions.map((t) => (
                  <option key={t.id} value={t.id}>{t.name}</option>
                ))}
              </Field>

              <Field
                as="select"
                name="body_id"
                className="form-input"
                onChange={e => {
                  const value = e.target.value ? parseInt(e.target.value, 10) : "";
                  setFieldValue('body_id', value); // используем setFieldValue
                }}
              >
                <option value="">Тип кузова</option>
                {bodies.map((b) => (
                  <option key={b.id} value={b.id}>{b.name}</option>
                ))}
              </Field>

              <Field name="year_of_issue" type="date" className="form-input" />

              <Field
                as="select"
                name="engine_type_id"
                className="form-input"
                onChange={e => {
                  const value = e.target.value ? parseInt(e.target.value, 10) : "";
                  setFieldValue('engine_type_id', value); // используем setFieldValue
                }}
              >
                <option value="">Тип двигателя</option>
                {engineTypes.map((e) => (
                  <option key={e.id} value={e.id}>{e.name}</option>
                ))}
              </Field>

              <Field
                as="select"
                name="drive_id"
                className="form-input"
                onChange={e => {
                  const value = e.target.value ? parseInt(e.target.value, 10) : "";
                  setFieldValue('drive_id', value); // используем setFieldValue
                }}
              >
                <option value="">Тип привода</option>
                {driveTypes.map((d) => (
                  <option key={d.id} value={d.id}>{d.name}</option>
                ))}
              </Field>

              <Field name="mileage" type="number" placeholder="Пробег" className="form-input" />
              <Field name="price" type="number" placeholder="Цена" className="form-input" />

              <Field
                as="select"
                name="rental_class_id"
                className="form-input"
                onChange={e => {
                  const value = e.target.value ? parseInt(e.target.value, 10) : "";
                  setFieldValue('rental_class_id', value); // используем setFieldValue
                }}
              >
                <option value="">Класс аренды</option>
                {rentalClasses.map((r) => (
                  <option key={r.id} value={r.id}>{r.name}</option>
                ))}
              </Field>

              <Field name="number_of_seats" type="number" placeholder="Кол-во мест" className="form-input" />
              <Field name="trunk_volume" type="number" placeholder="Объём багажника" className="form-input" />

              <button type="submit" className="col-span-3 bg-blue-600 text-white py-2 rounded">
                Добавить
              </button>
            </Form>
          )}
        </Formik>
      </div>

      <div className="bg-white p-6 rounded-xl shadow">
        <h2 className="text-xl font-bold mb-4">Список автомобилей</h2>
        <table className="table-auto border-separate border-spacing-y-4 w-full">
          <thead>
            <tr>
              <th>ID</th>
              <th>Модель</th>
              <th>Бренд</th>
              <th>Цена за час</th>
              <th>Год</th>
            </tr>
          </thead>
          <tbody>
            {cars.map((car) => (
              <tr key={car.id} className="bg-white shadow rounded-lg">
                <td className="text-center">{car.id}</td>
                <td className="text-center">{car.model}</td>
                <td className="text-center">{car.car_brand?.name}</td>
                <td className="text-center">{car.price} ₽</td>
                <td className="text-center">{new Date(car.year_of_issue).getFullYear()}</td>
                <td className="text-center">
                  <button className="bg-red-600 text-white px-4 rounded-lg" onClick={() => onCarDelete(car.id)}>Удалить</button>
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
