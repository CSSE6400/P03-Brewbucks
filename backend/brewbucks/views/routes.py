from flask import Blueprint, jsonify,request
from brewbucks.models import db
from brewbucks.models.users import Users
from brewbucks.models.users import Roles
api = Blueprint('api', __name__, url_prefix='/api/v1')

@api.route('/health', methods=['GET'])
def health():
        return jsonify({"status":"Healthy"}),200

@api.route('/users_test', methods=['GET'])
def create_test_user():
    user = Users(first_name='John', last_name='Doe', password='password', username='johndoe')
#     print(user.to_dict())
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@api.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    password = data.get('password')
    username = data.get('username')
    role = data.get('role', Roles.Customer)  # default to Customer if role is not provided

    if not all([first_name, last_name, password, username]):
        return jsonify({'error': 'Missing required parameters'}), 400

    try:
        role_enum = Roles(role)
    except ValueError:
        return jsonify({'error': 'Invalid role provided'}), 400

    user = Users(
        first_name=first_name,
        last_name=last_name,
        password=password,
        username=username,
        role=role_enum
    )

    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201