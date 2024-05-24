from flask import Blueprint, jsonify, request
from brewbucks.models import db
from brewbucks.models.users import Users, Roles
from brewbucks.models.order import Orders, OrderStatus
from brewbucks.models.payments import PaymentStatus
from brewbucks.models.menu_item import MenuItems
from brewbucks.models.order_items import OrderItems
from brewbucks.models.rewards import Rewards

api = Blueprint('api', __name__, url_prefix='/api/v1')

# Health check route to ensure the API is running
@api.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "Healthy"}), 200

# Route to create a test user for testing purposes
@api.route('/users_test', methods=['GET'])
def create_test_user():
    user = Users(first_name='John', last_name='Doe', password='password', username='johndoe')
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

# Route to create a new user
@api.route('/users', methods=['POST'])
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

    try:
        role_enum = Roles(role)
    except ValueError:
        return jsonify({'error': 'Invalid role provided'}), 400

    user = Users(first_name=first_name, last_name=last_name, password=password, username=username, role=role_enum)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

# route to check login 
@api.route('users/login',methods = ['POST'])

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

# Route to get a user by their user ID
@api.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = Users.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200

# Route to update a user by their user ID
@api.route('/users', methods=['PUT'])
def update_user():
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
        user.username = data['username']
    if 'role' in data:
        try:
            role_enum = Roles(data['role'])
            user.role = role_enum
        except ValueError:
            return jsonify({'error': 'Invalid role provided'}), 400

    db.session.commit()
    return jsonify(user.to_dict()), 200

# Route to get all orders for a specific user
@api.route('/users/<int:user_id>/orders', methods=['GET'])
def get_user_orders(user_id):
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
    total = data.get('total')
    payment_status = data.get('payment_status', PaymentStatus.Pending)  # Defaults to pending
    order_status = data.get('order_status', OrderStatus.Processing)  # Defaults to processing
    rewards_added = data.get('rewards_added', 0)  # Defaults to 0 points

    if (total,user_id) is None:
        return jsonify({'error': 'Missing required parameter: total'}), 400
    
    user = Users.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    try:
        payment_status_enum = PaymentStatus(payment_status)
    except ValueError:
        return jsonify({'error': 'Invalid payment status provided'}), 400

    try:
        order_status_enum = OrderStatus(order_status)
    except ValueError:
        return jsonify({'error': 'Invalid order status provided'}), 400

    new_order = Orders(user_id=user_id, total=total, payment_status=payment_status_enum, order_status=order_status_enum, rewards_added=rewards_added)
    db.session.add(new_order)
    db.session.commit()
    return jsonify(new_order.to_dict()), 201

# Route to delete a user by their user ID
@api.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = Users.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

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
    
    user = Users.query.get(user_id = user_id, role = "employee")
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
    item = MenuItems.query.get(item_id)
    if item is None:
        return jsonify({'error': 'Menu item not found'}), 404

    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    
    user_id= data.get("user_id")
    
    if not all([user_id is not None]):
        return jsonify({'error': 'Missing required parameter : user_id'}), 400
    
    user = Users.query.get(user_id = user_id,role = "employee")
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
@api.route('/menu_items/<int:item_id>', methods=['DELETE'])
def delete_menu_item(item_id):
    item = MenuItems.query.get(item_id)
    if item is None:
        return jsonify({'error': 'Menu item not found'}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Menu item deleted successfully'}), 200

# Route to add order items to a specific order for a user
@api.route('/users/<int:user_id>/orders/<int:order_id>/items', methods=['POST'])
def add_order_items(user_id, order_id):
    user = Users.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    order = Orders.query.filter_by(order_id=order_id, user_id=user_id).first()
    if not order:
        return jsonify({'error': 'Order not found for the user'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    order_items = data.get('order_items')
    if not order_items or not isinstance(order_items, list):
        return jsonify({'error': 'Invalid or missing order_items parameter'}), 400

    created_items = []
    for item in order_items:
        menu_item_id = item.get('menu_item_id')
        quantity = item.get('quantity', 1)

        if not menu_item_id:
            return jsonify({'error': 'Missing required parameter: menu_item_id'}), 400

        menu_item = MenuItems.query.get(menu_item_id)
        if not menu_item:
            return jsonify({'error': f'Menu item with id {menu_item_id} not found'}), 404

        new_order_item = OrderItems(order_id=order_id, menu_item_id=menu_item_id, quantity=quantity)
        db.session.add(new_order_item)
        db.session.flush()  # Ensure the ID is generated before committing
        created_items.append(new_order_item.to_dict())

    db.session.commit()
    return jsonify(created_items), 201

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
