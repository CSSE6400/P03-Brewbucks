import Coffee from "./Coffee"
import Store from "./Store"

const Menu = () => {
    return (
        <div className="flex-row space-y-2">
            <Store></Store>
            <Coffee name="Iced Latte" desc="This is a description about a iced latte" price="$7.50"></Coffee>
            <Coffee name="mocha" desc="mocha description" price="$7.50"></Coffee>
            <Coffee name="americano" desc="americano description" price="$7.50"></Coffee>
        </div>
    )
}

export default Menu;