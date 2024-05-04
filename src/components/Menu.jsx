import Coffee from "./Coffee"
import Store from "./Store"

const Menu = () => {
    return (
        <div className="flex-col space-y-3">
            <Store></Store>
            <div className="flex-col space-y-1.5">
                <Coffee name="Iced Latte" desc="This is a description about an Iced Latte" price="$7.50"></Coffee>
                <Coffee name="Mocha" desc="This is a description about a Mocha" price="$7.50"></Coffee>
                <Coffee name="Americano" desc="This is a description about an Americano" price="$7.50"></Coffee>
            </div>
        </div>
    )
}

export default Menu;