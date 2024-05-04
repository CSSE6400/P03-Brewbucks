

const Store = () => {
    return (
        <div className="bg-white shadow-sm p-5 rounded-lg flex justify-between">
            <div className="">
                <p className="text-xl font-medium">Coffee Shop</p>
                <div className="rating mt-2 rating-xs">
                    <input type="radio" name="rating-5" className="mask mask-star-2 bg-indigo-900" />
                    <input type="radio" name="rating-5" className="mask mask-star-2 bg-indigo-900" />
                    <input type="radio" name="rating-5" className="mask mask-star-2 bg-indigo-900" />
                    <input type="radio" name="rating-5" className="mask mask-star-2 bg-indigo-900" />
                    <input type="radio" name="rating-5" className="mask mask-star-2 bg-indigo-900" checked/>
                </div>
                <p className="text-sm mt-0.5">St Lucia, 4072, Queensland, Australia</p>
            </div>
            <div className="flex-col items-start space-y-1.5">
                <p className="font-bold text-green-400 text-sm pl-4">We are open!</p>
            </div>
        </div>
    )
}

export default Store;