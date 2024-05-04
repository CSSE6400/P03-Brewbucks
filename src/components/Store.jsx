import { Rating } from "flowbite-react";

const Store = () => {
    return (
        <div className="bg-white shadow-sm p-6 rounded-lg flex justify-between">
            <div className="">
                <p className="text-xl font-medium">Coffee Shop</p>
                <Rating className="mt-2">
                    <Rating.Star className="mt-0.5" />
                    <p className="ml-1 text-sm font-bold text-gray-900 dark:text-white">4.95</p>
                    <span className="mx-1.5 mt-2 h-1 w-1 rounded-full bg-gray-500 dark:bg-gray-400" />
                    <a href="#" className="text-sm font-medium text-gray-900 underline hover:no-underline dark:text-white">
                        73 reviews
                    </a>
                </Rating>
                <p className="text-sm mt-1">St Lucia, 4072, Queensland, Australia</p>
            </div>
            <div className="flex-col items-start space-y-1.5">
                <p className="font-bold text-green-400 text-sm pl-4">We are open!</p>
            </div>
        </div>
    )
}

export default Store;