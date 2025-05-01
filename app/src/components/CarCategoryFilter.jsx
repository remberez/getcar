import { useEffect, useState } from "react";
import rentalClass from "../serives/rentalClass";

export default function CarCategoryFilter({ onChange }) {
    const [active, setActive] = useState({});
    const [rentalClasses, setRentalClasses] = useState([]);
  
    useEffect(() => {
        async function fetchData() {
            const data = await rentalClass.getList();
            setRentalClasses(data);
        }
        fetchData();
    }, []);

    const handleClick = (category) => {
        setActive(category);
        onChange?.(category);
    };

    return (
        <div className="w-full flex flex-col items-start gap-4 container mt-12">
        <div className="bg-red-600 text-white font-bold uppercase text-center px-6 py-3 text-sm rounded">
            Аренда авто в Саратове
        </div>
        <div className="flex flex-wrap gap-3">
            {rentalClasses?.map((cat) => {
            const isActive = cat === active;
            return (
                    <button
                    key={cat.id}
                    onClick={() => handleClick(cat)}
                    className={`flex items-center gap-1 px-5 py-2 rounded-full text-sm font-medium transition
                        ${isActive
                        ? "border border-black text-black bg-white"
                        : "bg-gray-100 text-black hover:bg-gray-200"}
                    `}
                    >
                    { cat.name }
                    <div>+</div>
                    </button>
                );
            })}
        </div>
        </div>
    );
}
