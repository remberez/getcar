import { useEffect, useState } from "react";
import CarCardList from "../components/CarCardsList";
import CarCategoryFilter from "../components/CarCategoryFilter";
import carService from "../serives/cars";

const SearchPage = () => {
    const [carList, setCarList] = useState([]);

    useEffect(() => {
        async function fetchData() {
            const data = await carService.getAllCars({});
            setCarList(data);
        }

        fetchData();
    }, [])

    async function onFilterChange(category) {
        const data = await carService.getAllCars({ category_id: category.id });
        setCarList(data);
    }

    return (
        <>
            <CarCategoryFilter onChange={onFilterChange}/>
            <CarCardList carList={carList}/>
        </>
    )
}

export default SearchPage;