from flask import Blueprint, jsonify, request
from datetime import datetime,timezone
from brewbucks.models import db
from brewbucks.models.users import Users, Roles
from brewbucks.models.order import Orders, OrderStatus
from brewbucks.models.payments import PaymentStatus,Payments
from brewbucks.models.menu_item import MenuItems
from brewbucks.models.order_items import OrderItems
from brewbucks.models.rewards import Rewards


api = Blueprint("api", __name__, url_prefix="/api/v1")


@api.route("/health", methods=["GET"]) #done
def health():
    return jsonify({"status": "Healthy"}), 200


@api.route("/users_test", methods=["POST"]) #done
def create_test_user():
    user = Users(
        first_name="John", last_name="Doe", password="password", username="johndoe"
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

###User routes###

# Route to create a new user
@api.route('/users', methods=['POST']) #done
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    password = data.get('password')
    username = data.get('username')
    role = data.get('role', Roles.Customer)  # Default to Customer if role is not provided

    if not all([first_name, last_name, password, username]):
        return jsonify({'error': 'Missing required parameters'}), 400

    existing_user = Users.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 400

    try:
        role_enum = Roles(role)
    except ValueError:
        return jsonify({'error': 'Invalid role provided'}), 400

    user = Users(first_name=first_name, last_name=last_name, password=password, username=username, role=role_enum)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

# route to check login 
@api.route('users/login',methods = ['POST']) #done

def login():
    data = request.json
    username = data.get("username")
    password= data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400
    
    user = Users.query.filter_by(username=username,password=password).first()

    if user is None:
        return jsonify({"error":"Invalid username or password"}), 401
    return jsonify({
            "message": "Login successful",
            "user": user.to_dict()
        }), 200

#route to get user_id
@api.route('users/user_id',methods= ['POST']) #done

def user_id():
    data = request.json
    username = data.get("username")

    if username == None:
        return jsonify({"message": "Username is required"}), 400
    
     
    user = Users.query.filter_by(username=username).first()

    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"user_id":user.user_id}),200
    
# Route to get a user by their user ID
@api.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
#     data = request.json
#     user_id=data.get("user_id")
    user = Users.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200

# Route to update a user by their user ID
@api.route('/users', methods=['PUT']) #done
def update_user_info():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({'error': 'Missing required parameter: user_id'}), 400

    user = Users.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'password' in data:
        user.password = data['password']
    if 'username' in data:
        username = data.get('username')
        existing_user = Users.query.filter_by(Users.username==username).first()
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 400
        user.username = data['username']
    if 'role' in data:
        try:
            role_enum = Roles(data['role'])
            user.role = role_enum
        except ValueError:
            return jsonify({'error': 'Invalid role provided'}), 400

    db.session.commit()
    return jsonify(user.to_dict()), 200

# Route to delete a user by their user ID
@api.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # data = request.json
    # user_id = data.get("user_id")
    user = Users.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

###Order routes###

#route to get all active orders(user specific)
@api.route('/orders/active', methods=['GET'])
def get_active_orders():
    data = request.json
    user_id = data.get("user_id")
    try:
        active_orders = Orders.query.filter(Orders.order_status.in_([OrderStatus.Processing, OrderStatus.Making]),Orders.user_id==user_id).all()
        active_orders_list = [order.to_dict() for order in active_orders]
        return jsonify(active_orders_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#route to get all finished orders
@api.route('/orders/finished', methods=['GET'])
def get_finished_orders():
    user_id = request.args.get('user_id')
    try:
        finished_orders = Orders.query.filter(Orders.order_status.in_([OrderStatus.Completed]),Orders.user_id==user_id).all()
        finished_orders_list = [order.to_dict() for order in finished_orders]
        return jsonify(finished_orders_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#route to get all making orders for a user
@api.route('/orders/making', methods=['GET'])
def get_making_orders():
    user_id = request.args.get('user_id')
    try:
        making_orders = Orders.query.filter(Orders.order_status.in_([OrderStatus.Making]),Orders.user_id==user_id).all()
        making_orders_list = [order.to_dict() for order in making_orders]
        return jsonify(making_orders_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#route to get all making orders for the diaply screen
@api.route('/orders/display_screen', methods=['GET'])
def get_making_orders_all():
    try:
        making_orders_all = Orders.query.filter(Orders.order_status.in_([OrderStatus.Making])).all()
        making_orders_all_list = [order.to_dict() for order in making_orders_all]
        return jsonify(making_orders_all_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to get all orders for a specific user
@api.route('/users/orders', methods=['GET'])
def get_user_orders():
    data = request.json
    user_id = data.get("user_id")
    user = Users.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    orders = Orders.query.filter_by(user_id=user_id).all()
    orders_list = [order.to_dict() for order in orders]
    return jsonify(orders_list), 200

# Route to create a new order for a specific user
@api.route('/users/orders', methods=['POST'])
def create_user_order():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    
    user_id = data.get("user_id")
    
    user = Users.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    order_items = data.get('order_items')  # Expecting a list of items

    if user_id is None or not order_items or not isinstance(order_items, list):
        return jsonify({'error': 'Missing required parameters: user_id or order_items'}), 400
    

    payment_status = PaymentStatus.Pending
    order_status = OrderStatus.Making
    rewards_added = 10

    # Overriding values
    if 'payment_status' in data:
        try:
            payment_status = PaymentStatus(data['payment_status'])
        except ValueError:
            return jsonify({'error': 'Invalid payment status provided'}), 400

    if 'order_status' in data:
        try:
            order_status = OrderStatus(data['order_status'])
        except ValueError:
            return jsonify({'error': 'Invalid order status provided'}), 400

    if 'rewards_added' in data:
        rewards_added = data['rewards_added']

    total = 0
    for item in order_items:
        menu_item_id = item.get('item_id')
        quantity = item.get('quantity', 1)

        if not menu_item_id:
            return jsonify({'error': 'Missing required parameter: menu_item_id'}), 400

        menu_item = MenuItems.query.get(menu_item_id)
        if not menu_item:
            return jsonify({'error': f'Menu item with id {menu_item_id} not found'}), 404

        total += menu_item.price * quantity

    new_order = Orders(user_id=user_id, total=total, payment_status=payment_status, order_status=order_status, rewards_added=rewards_added)
    db.session.add(new_order)
    db.session.flush()  # Ensure the order ID is generated before adding order items

    created_items = []
    for item in order_items:
        menu_item_id = item.get('item_id')
        quantity = item.get('quantity', 1)

        new_order_item = OrderItems(order_id=new_order.order_id, menu_item_id=menu_item_id, quantity=quantity)
        db.session.add(new_order_item)
        db.session.flush()  # Ensure the ID is generated before committing
        created_items.append(new_order_item.to_dict())

    # Create a payment entry for the new order
    new_payment = Payments(
        order_id=new_order.order_id,
        payment_method='Demo Checkout',
        payment_status=PaymentStatus.Pending,
        payment_date=datetime.now(timezone.utc),
        amount=total,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    db.session.add(new_payment)

    # Update or create rewards for the user
    rewards_record = Rewards.query.filter_by(customer_id=user_id).first()
    if rewards_record:
        rewards_record.total_points += rewards_added
        rewards_record.updated_at = datetime.now(timezone.utc)
    else:
        rewards_record = Rewards(
            customer_id=user_id,
            total_points=rewards_added,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        db.session.add(rewards_record)

    db.session.commit()
    return jsonify({
        'order': new_order.to_dict(),
        'order_items': created_items,
        'payment': new_payment.to_dict()
    }), 201


# Route to update an existing order for a specific user
@api.route('/users/orders', methods=['PUT'])
def update_user_order():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    
    user_id = data.get("user_id")
    order_id = data.get("order_id")
    
    if user_id is None or order_id is None:
        return jsonify({'error': 'Missing required parameters: user_id or order_id'}), 400
    
    user = Users.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    order = Orders.query.get(order_id)
    if order is None:
        return jsonify({'error': 'Order not found'}), 404

    if order.user_id != user_id:
        return jsonify({'error': 'User ID does not match the order'}), 403

    # Overriding values if provided
    if 'order_status' in data:
        try:
            order.order_status = OrderStatus(data['order_status'])
        except ValueError:
            return jsonify({'error': 'Invalid order status provided'}), 400

    if 'rewards_added' in data:
        order.rewards_added = data['rewards_added']    

    # Update order items if provided
    if 'order_items' in data:
        order_items = data['order_items']
        if not isinstance(order_items, list):
            return jsonify({'error': 'Invalid order_items parameter, expected a list'}), 400

        # Clear existing order items
        OrderItems.query.filter_by(order_id=order_id).delete()

        total = 0
        created_items = []
        for item in order_items:
            menu_item_id = item.get('item_id')
            quantity = item.get('quantity', 1)

            if not menu_item_id:
                return jsonify({'error': 'Missing required parameter: menu_item_id'}), 400

            menu_item = MenuItems.query.get(menu_item_id)
            if not menu_item:
                return jsonify({'error': f'Menu item with id {menu_item_id} not found'}), 404

            total += menu_item.price * quantity

            new_order_item = OrderItems(order_id=order_id, menu_item_id=menu_item_id, quantity=quantity)
            db.session.add(new_order_item)
            db.session.flush()  # Ensure the ID is generated before committing
            created_items.append(new_order_item.to_dict())

        order.total = total
    else:
        created_items = [item.to_dict() for item in OrderItems.query.filter_by(order_id=order_id).all()]

    order.updated_at = datetime.now(timezone.utc)

    # Update payment information
    payment = Payments.query.filter_by(order_id=order_id).first()
    if payment:
        if 'payment_status' in data:
            try:
                payment_status_enum = PaymentStatus(data['payment_status'])
            except ValueError:
                return jsonify({'error': 'Invalid payment status provided'}), 400

            order.payment_status = payment_status_enum
            payment.payment_status = payment_status_enum

        payment.amount = order.total
        payment.updated_at = datetime.now(timezone.utc)
    else:
        return jsonify({'error': 'Payment record not found'}), 404

    # Update or create rewards for the user
    rewards_added = data.get('rewards_added', order.rewards_added)
    rewards_record = Rewards.query.filter_by(customer_id=user_id).first()
    if rewards_record:
        rewards_record.total_points += rewards_added
        rewards_record.updated_at = datetime.now(timezone.utc)
    else:
        rewards_record = Rewards(
            customer_id=user_id,
            total_points=rewards_added,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        db.session.add(rewards_record)

    db.session.commit()

    return jsonify({
        'order': order.to_dict(),
        'order_items': created_items,
        'payment': payment.to_dict(),
        'rewards': rewards_record.to_dict()
    }), 200

# Route to delete a order by its order ID
@api.route('/users/orders', methods=['DELETE'])
def delete_order():
    data = request.json
    order_id = data.get("order_id")
    if order_id is None:
        return jsonify({'error': 'Missing required parameter: order_id'}), 400
    order = Orders.query.get(order_id)
    if order is None:
        return jsonify({'error': 'order not found'}), 404
    
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'order deleted successfully'}), 200

''' 

 Menu routes

'''
# Route to test menu items 
@api.route('/test_menuitems', methods=['POST'])
def create_test_menu_items():
    test_menu_items = [
        {
            'name': 'Latte',
            'description': 'A delicious coffee drink',
            'price': 4.50,
            'orderable': True
        },
        {
            'name': 'Espresso',
            'description': 'Strong and bold coffee',
            'price': 3.00,
            'orderable': True
        },
        {
            'name': 'Cappuccino',
            'description': 'Coffee with steamed milk foam',
            'price': 4.00,
            'orderable': True
        },
        {
            'name': 'Americano',
            'description': 'Espresso with hot water',
            'price': 3.50,
            'orderable': True
        },
        {
            'name': 'Mocha',
            'description': 'Coffee with chocolate',
            'price': 4.75,
            'orderable': True
        },
    ]

    for item in test_menu_items:
        new_item = MenuItems(
            name=item['name'],
            description=item['description'],
            price=item['price'],
            orderable=item['orderable']
        )
        db.session.add(new_item)

    db.session.commit()
    return jsonify({'message': 'Test menu items created successfully'}), 201

# Route to get all menu items
@api.route('/menu_items', methods=['GET'])
def get_menu_items():
    menu_items = MenuItems.query.all()
    return jsonify([item.to_dict() for item in menu_items]), 200

# Route to get a specific menu item by its ID
@api.route('/menu_items/<int:item_id>', methods=['GET'])
def get_menu_item(item_id):
    item = MenuItems.query.get(item_id)
    if item is None:
        return jsonify({'error': 'Menu item not found'}), 404
    return jsonify(item.to_dict()), 200

# Route to create a new menu item
@api.route('/menu_items', methods=['POST'])
def create_menu_item():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    
    user_id = data.get('user_id')
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    orderable = data.get('orderable', True)

    if not all([user_id,name, description, price is not None]):
        return jsonify({'error': 'Missing required parameters'}), 400
    
    user = Users.query.filter_by(user_id = user_id, role = "employee")
    if user is None:
        return jsonify({'error': 'User access denied'}), 404
    
    # Ensure orderable is a boolean
    if isinstance(orderable, str):
        if orderable.lower() == 'true':
            orderable = True
        elif orderable.lower() == 'false':
            orderable = False
        else:
            return jsonify({'error': 'Invalid value for orderable'}), 400

    new_item = MenuItems(name=name, description=description, price=price, orderable=orderable)
    db.session.add(new_item)
    db.session.commit()
    return jsonify(new_item.to_dict()), 201

# Route to update a menu item by its ID
@api.route('/menu_items/<int:item_id>', methods=['PUT'])
def update_menu_item(item_id):
    # data= request.json
    # item_id = data.get("item_id")
    item = MenuItems.query.get(item_id)
    if item is None:
        return jsonify({'error': 'Menu item not found'}), 404

    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    
    user_id= data.get("user_id")
    
    if not all([user_id is not None]):
        return jsonify({'error': 'Missing required parameter : user_id'}), 400
    
    user = Users.query.filter_by(user_id = user_id,role = "employee")
    if user is None:
        return jsonify({'error':'User access denied'}),400
    
    if 'name' in data:
        item.name = data['name']
    if 'description' in data:
        item.description = data['description']
    if 'price' in data:
        item.price = data['price']
    if 'orderable' in data:
        orderable = data['orderable']
        if isinstance(orderable, str):
            if orderable.lower() == 'true':
                item.orderable = True
            elif orderable.lower() == 'false':
                item.orderable = False
            else:
                return jsonify({'error': 'Invalid value for orderable'}), 400
        else:
            item.orderable = orderable

    db.session.commit()
    return jsonify(item.to_dict()), 200

# Route to delete a menu item by its ID
@api.route('/menu_items', methods=['DELETE'])
def delete_menu_item():
    data = request.json
    user_id = data.get("user_id")
    item_id = data.get("item_id")
    
    if not user_id or not item_id:
        return jsonify({'error': 'Missing required parameter: user_id or item_id'}), 400
    
    user = Users.query.filter_by(user_id=user_id, role="employee")
    
    if user is None:
        return jsonify({'error': 'User access denied'}), 403
    
    item = MenuItems.query.get(item_id)
    
    if item is None:
        return jsonify({'error': 'Menu item not found'}), 404
    
    db.session.delete(item)
    db.session.commit()
    
    return jsonify({'message': 'Menu item deleted successfully'}), 200

##Routes for orderItems##

# Route to get all items in an order for a specific user and order
@api.route('/users/<int:user_id>/orders/<int:order_id>/items', methods=['GET'])
def get_order_items(user_id, order_id):
    order = Orders.query.filter_by(order_id=order_id, user_id=user_id).first()
    if not order:
        return jsonify({'error': 'Order not found for the user'}), 404

    order_items = OrderItems.query.filter_by(order_id=order_id).all()
    if not order_items:
        return jsonify({'error': 'No items found for this order'}), 404

    items_list = [item.to_dict() for item in order_items]
    return jsonify(items_list), 200

# Route to update an order item by its ID for a specific user and order
@api.route('/users/<int:user_id>/orders/<int:order_id>/items/<int:order_item_id>', methods=['PUT'])
def update_order_item(user_id, order_id, order_item_id):
    user = Users.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    order = Orders.query.filter_by(order_id=order_id, user_id=user_id).first()
    if not order:
        return jsonify({'error': 'Order not found for the user'}), 404

    order_item = OrderItems.query.filter_by(order_item_id=order_item_id, order_id=order_id).first()
    if not order_item:
        return jsonify({'error': 'Order item not found for the order'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    if 'menu_item_id' in data:
        menu_item_id = data['menu_item_id']
        menu_item = MenuItems.query.get(menu_item_id)
        if not menu_item:
            return jsonify({'error': f'Menu item with id {menu_item_id} not found'}), 404
        order_item.menu_item_id = menu_item_id

    if 'quantity' in data:
        order_item.quantity = data['quantity']

    db.session.commit()
    return jsonify(order_item.to_dict()), 200

# Route to delete an order item by its ID for a specific user and order
@api.route('/users/<int:user_id>/orders/<int:order_id>/items/<int:order_item_id>', methods=['DELETE'])
def delete_order_item(user_id, order_id, order_item_id):
    user = Users.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    order = Orders.query.filter_by(order_id=order_id, user_id=user_id).first()
    if not order:
        return jsonify({'error': 'Order not found for the user'}), 404

    order_item = OrderItems.query.filter_by(order_item_id=order_item_id, order_id=order_id).first()
    if not order_item:
        return jsonify({'error': 'Order item not found for the order'}), 404

    db.session.delete(order_item)
    db.session.commit()
    return jsonify({'message': 'Order item deleted successfully'}), 200

#Routes for Rewards
# Route to get all rewards for a specific user
@api.route('/users/rewards', methods=['GET'])
def user_rewards():
    user_id = request.args.get('user_id')
    user = Users.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    rewards = Rewards.query.filter_by(customer_id=user_id).all()
    return jsonify({"User points":[reward.total_points for reward in rewards],"Rewards details":[reward.to_dict() for reward in rewards]}), 200



#Removed routes

# Route to add order items to a specific order for a user
# @api.route('/users/orders/items', methods=['POST']) 
# def add_order_items():

#     data = request.get_json()
#     if not data:
#         return jsonify({'error': 'No input data provided'}), 400
#     user_id = data.get("user_id")
#     order_id = data.get("order_id")
#     user = Users.query.get(user_id)
#     if user is None:
#         return jsonify({'error': 'User not found'}), 404

#     order = Orders.query.filter_by(order_id=order_id, user_id=user_id).first()
#     if not order:
#         return jsonify({'error': 'Order not found for the user'}), 404

#     order_items = data.get('order_items')
#     if not order_items or not isinstance(order_items, list):
#         return jsonify({'error': 'Invalid or missing order_items parameter'}), 400

#     created_items = []
#     for item in order_items:
#         menu_item_id = item.get('menu_item_id')
#         quantity = item.get('quantity', 1)

#         if not menu_item_id:
#             return jsonify({'error': 'Missing required parameter: menu_item_id'}), 400

#         menu_item = MenuItems.query.get(menu_item_id)
#         if not menu_item:
#             return jsonify({'error': f'Menu item with id {menu_item_id} not found'}), 404

#         new_order_item = OrderItems(order_id=order_id, menu_item_id=menu_item_id, quantity=quantity)
#         db.session.add(new_order_item)
#         db.session.flush()  # Ensure the ID is generated before committing
#         created_items.append(new_order_item.to_dict())

#     db.session.commit()
#     return jsonify(created_items), 201


# # Route to create a new order item based on menu item id
# @api.route('/order_items', methods=['POST'])
# def create_order_item():
#     data = request.get_json()
#     if not data:
#         return jsonify({'error': 'No input data provided'}), 400
    
#     user_id = data.get('user_id')
#     order_id = data.get('order_id')
#     menu_item_id = data.get('menu_item_id')
#     quantity = data.get('quantity', 1)

#     if not all([user_id, order_id, menu_item_id, quantity]):
#         return jsonify({'error': 'Missing required parameters'}), 400

#     user = Users.query.filter_by(user_id=user_id).first()
#     if user is None:
#         return jsonify({'error': 'User not found'}), 404
    
#     order = Orders.query.filter_by(order_id=order_id, user_id=user_id).first()
#     if order is None:
#         return jsonify({'error': 'Order not found'}), 404

#     menu_item = MenuItems.query.filter_by(item_id=menu_item_id, orderable=True).first()
#     if menu_item is None:
#         return jsonify({'error': 'Menu item not found or not orderable'}), 404

#     new_order_item = OrderItems(order_id=order_id, menu_item_id=menu_item_id, quantity=quantity)
#     db.session.add(new_order_item)
#     db.session.commit()
#     return jsonify(new_order_item.to_dict()), 201