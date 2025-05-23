import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { observer } from "mobx-react-lite";
import authStore from "../store/authStore";
import bookingService from "../serives/bookingService";

const CarBookingModal = observer(function CarBookingModal({ car, isOpen, onClose }) {
  const [dateStart, setDateStart] = useState("");
  const [dateEnd, setDateEnd] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    if (isOpen && !authStore.isAuth) {
      onClose();
      navigate("/login");
    }
    // eslint-disable-next-line
  }, [isOpen]);

  if (!isOpen || !car) return null;

  const handleBooking = async () => {
    setLoading(true);
    setError("");
    try {
      await bookingService.createBooking({
        car_id: car.id,
        date_start: dateStart,
        date_end: dateEnd,
      });
      setSuccess(true);
    } catch (e) {
      setError(e?.response?.data?.detail || "Ошибка бронирования");
    }
    setLoading(false);
  };

  const handleClose = () => {
    setDateStart("");
    setDateEnd("");
    setError("");
    setSuccess(false);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40">
      <div className="bg-white rounded-xl shadow-lg p-6 w-full max-w-md relative">
        <button
          className="absolute top-2 right-2 text-gray-400 hover:text-gray-700 text-2xl"
          onClick={handleClose}
        >
          ×
        </button>
        <h2 className="text-xl font-bold mb-4">Аренда {car.car_brand?.name} {car.model}</h2>
        <div className="mb-2 text-gray-700">
          <div>Класс: <b>{car.rental_class?.name}</b></div>
          <div>Коробка: <b>{car.transmission?.name}</b></div>
          <div>Двигатель: <b>{car.engine_type?.name}</b></div>
          <div>Цена: <b>{car.price} ₽/сутки</b></div>
        </div>
        <div className="mb-4">
          <label className="block text-sm mb-1">Дата начала аренды</label>
          <input
            type="datetime-local"
            className="w-full border rounded px-3 py-2"
            value={dateStart}
            onChange={e => setDateStart(e.target.value)}
          />
        </div>
        <div className="mb-4">
          <label className="block text-sm mb-1">Дата конца аренды</label>
          <input
            type="datetime-local"
            className="w-full border rounded px-3 py-2"
            value={dateEnd}
            onChange={e => setDateEnd(e.target.value)}
          />
        </div>
        {error && <div className="text-red-600 mb-2">{error}</div>}
        {success ? (
          <div className="text-green-600 font-semibold mb-2">Бронирование успешно!</div>
        ) : (
          <button
            className="w-full bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded transition"
            onClick={handleBooking}
            disabled={loading || !dateStart || !dateEnd}
          >
            {loading ? "Бронирование..." : "Подтвердить аренду"}
          </button>
        )}
      </div>
    </div>
  );
});

export default CarBookingModal;