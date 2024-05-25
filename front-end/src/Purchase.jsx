import "./styles.css"

const Purchase = () => {
    return (
        <div>
            <div className="custom-background p-4 h-screen flex justify-center items-center">
                <div className="bg-white rounded-2xl p-10 flex-col space-y-10 shadow-xl">
                    <div id="heading">
                        <p className="text-3xl text-indigo-900 font-bold">Confirm Your Purchase</p> 
                    </div>

                    <div id="buttons" className="flex justify-center space-x-4">
                        <button className="btn btn-sm rounded-lg bg-green-600 p-2 content-center w-1/4">
                            <p className="text-white font-bold">
                                Success
                            </p>
                        </button> 
                        <button className="btn btn-sm rounded-lg bg-red-600 p-2 content-center w-1/4">
                            <p className="text-white font-bold">
                                Fail
                            </p>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Purchase;
