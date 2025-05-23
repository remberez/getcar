import { api } from ".";

class BookingService {
    async createBooking({ car_id, date_start, date_end }) {
        try {
            const response = await api.post("/booking/", {
                car_id,
                date_start,
                date_end,
            });
            return response.data;
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    async getUserBookings() {
        try {
            const response = await api.get("/booking/");
            return response.data;
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    async getBookingById(id) {
        try {
            const response = await api.get(`/booking/${id}`);
            return response.data;
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    async updateBooking(id, payload) {
        try {
            const response = await api.patch(`/booking/${id}`, payload);
            return response.data;
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    async deleteBooking(id) {
        try {
            const response = await api.delete(`/booking/${id}`);
            return response.data;
        } catch (error) {
            console.error(error);
            throw error;
        }
    }
}

const bookingService = new BookingService();
export default bookingService;