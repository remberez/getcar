import { useEffect, useState } from "react";
import bookingService from "../serives/bookingService";

const MyBookingsPage = () => {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchBookings() {
      try {
        const data = await bookingService.getUserBookings();
        setBookings(data);
      } finally {
        setLoading(false);
      }
    }
    fetchBookings();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-[60vh]">
        <div className="text-lg text-gray-600">Загрузка бронирований...</div>
      </div>
    );
  }

  if (!bookings.length) {
    return (
      <div className="max-w-2xl mx-auto px-6 py-10 bg-white shadow-md rounded-xl text-center">
        <h2 className="text-2xl font-bold mb-4">Мои аренды</h2>
        <div className="text-gray-600">У вас пока нет активных бронирований.</div>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto px-6 py-10 bg-white shadow-md rounded-xl">
      <h2 className="text-2xl font-bold mb-6">Мои аренды</h2>
      <div className="space-y-6">
        {bookings.map((booking) => (
          <div key={booking.id} className="border rounded-lg p-4 shadow-sm bg-gray-50">
            <div className="flex flex-col md:flex-row md:justify-between md:items-center mb-2">
              <div>
                <div className="font-semibold text-lg">
                  {booking.car?.car_brand?.name} {booking.car?.model}
                </div>
                <div className="text-gray-600 text-sm">
                  {booking.car?.rental_class?.name} • {booking.car?.transmission?.name} • {booking.car?.engine_type?.name}
                </div>
              </div>
              <div className="mt-2 md:mt-0">
                <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
                  {new Date(booking.date_start).toLocaleString("ru-RU")} — {new Date(booking.date_end).toLocaleString("ru-RU")}
                </span>
              </div>
            </div>
            <div className="text-gray-700">
              Статус: <b>Активно</b>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MyBookingsPage;