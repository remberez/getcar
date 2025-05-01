import CarCard from "./CarCard,";

const CarCardList = ({ carList }) => {
    return (
        <section className="flex flex-col gap-y-10 mt-12 container">
            {
                carList?.map(value => (
                    <div key={value.id}>
                        <CarCard car={value}/>
                    </div>
                ))
            }
        </section>
    )
}

export default CarCardList;