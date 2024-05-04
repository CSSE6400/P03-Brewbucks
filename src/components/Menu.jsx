import Coffee from "./Coffee"
import Store from "./Store"

const Menu = ({handleClick}) => {
    return (
        <div className="flex-col space-y-3">
            <Store></Store>
            <div className="flex-col space-y-1.5">
                <Coffee handleClick={handleClick} name="Iced Latte" desc="This is a description about an Iced Latte" price="$7.50"></Coffee>
                <Coffee handleClick={handleClick} name="Mocha" desc="This is a description about a Mocha" price="$7.50"></Coffee>
                <Coffee handleClick={handleClick} name="Americano" desc="This is a description about an Americano" price="$7.50"></Coffee>
            </div>
        </div>
    )
}

export default Menu;