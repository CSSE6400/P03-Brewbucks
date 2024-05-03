import Coffee from "./Coffee"

const Menu = () => {
    return (
        <div className="outline p-2 flex-row space-y-2">
            <div >Menu:</div>
            <Coffee name="latte" desc="latte description" price="$7.50"></Coffee>
            <Coffee name="mocha" desc="mocha description" price="$7.50"></Coffee>
            <Coffee name="americano" desc="americano description" price="$7.50"></Coffee>
        </div>
    )
}

export default Menu;