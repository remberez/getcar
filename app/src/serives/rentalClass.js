import { api } from ".";

class RentalClass {
    async getList() {
        try {
            const response = await api.get("/rental-classes");
            return response.data;
        } catch (error) {
            console.error(error);
        }
    }
}

export default new RentalClass();