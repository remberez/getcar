import { api } from ".";

class CarService {
    async getAllCars({ offset, limit, brand_id, model, min_price, max_price, category_id }) {
        try {
            const response = await api.get("/cars", {
                params: {
                    offset,
                    limit,
                    brand_id,
                    model,
                    min_price,
                    max_price,
                    category_id
                }
            });
            return response.data;
        } catch (error) {
            console.error(error);
        }
    }

    async deleteCar(id) {
        try {
            const response = await api.delete(`/cars/${id}`);
            return response;
        } catch (error) {
            console.error(error);
        }
    }

    async createCar({car_brand_id, model, transmission_id, body_id, year_of_issue, engine_type_id, drive_id, mileage, price, rental_class_id, number_of_seats, trunk_volume}) {
        const response = await api.post("/cars/", {
            car_brand_id,
            model, 
            transmission_id,
            body_id,
            year_of_issue,
            engine_type_id,
            drive_id,
            mileage, 
            price, 
            rental_class_id, 
            number_of_seats,
            trunk_volume,
        })
        return response.data;
    }
}

const carService = new CarService();
export default carService;