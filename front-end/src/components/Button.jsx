const Button = ({text, click, width}) => {

    return (
        <div>
            <button onClick={click} className="btn btn-sm rounded-lg bg-indigo-900 p-2 content-center" style={{"width": width}}>
                <p className="text-white">
                    {text}
                </p>
            </button> 
        </div>
    )
}

export default Button;