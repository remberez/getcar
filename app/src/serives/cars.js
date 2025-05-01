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
}

const carService = new CarService();
export default carService;