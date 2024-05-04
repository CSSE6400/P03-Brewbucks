const Coffee = ({name, desc, price, handleClick}) => {
    return (
        <div className="bg-white shadow-sm p-5 rounded-md flex justify-between items-center">
            <div className="flex-col space-y-0.5">
                <p className="font-medium">{name}</p>
                <p className="text-sm">{desc}</p>
            </div>
            <div className="flex items-center space-x-3">
                <div>{price}</div>
                <button onClick={()=>handleClick({name, price})} className="btn btn-sm bg-indigo-900 p-1.5 content-center">
                    <p className="text-2xl text-white font-black pb-1">
                        +
                    </p>
                </button> 
            </div>
        </div>
    )
}

export default Coffee;