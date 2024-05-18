from flask import Blueprint, jsonify
from brewbucks.models import db
from brewbucks.models.users import Users

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