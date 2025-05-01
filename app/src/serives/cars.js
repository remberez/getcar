import { api } from ".";

class CarService {
    async getAllCars({ offset, limit, brand_id, model, min_price, max_price }) {
        try {
            const response = await api.get("/cars", {
                params: {
                    offset,
                    limit,
                    brand_id,
                    model,
                    min_price,
                    max_price
                }
            });
            return response.data;
        } catch (error) {
            console.error(error);
        }
    }
}

const carService = new CarService();
export default carService;