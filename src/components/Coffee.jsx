const Coffee = ({name, desc, price}) => {
    return (
        <div className="outline p-1">
            <div>{name}</div>
            <div>{desc}</div>
            <div>{price}</div>
        </div>
    )
}

export default Coffee;