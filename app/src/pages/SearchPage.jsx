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
    return (
        <>
            <CarCategoryFilter/>
            <CarCardList carList={carList}/>
        </>
    )
}

export default SearchPage;