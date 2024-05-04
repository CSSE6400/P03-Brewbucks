const Coffee = ({name, desc, price}) => {
    return (
        <div className="bg-white shadow-sm p-6 rounded-lg flex justify-between">
            <div>{name}</div>
            <div>{desc}</div>
            <div>{price}</div>
        </div>
    )
}

export default Coffee;