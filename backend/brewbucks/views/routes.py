from flask import Blueprint, jsonify, request
from brewbucks.models import db
from brewbucks.models.users import Users, Roles


api = Blueprint("api", __name__, url_prefix="/api/v1")


@api.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "Healthy"}), 200


@api.route("/users_test", methods=["POST"])
def create_test_user():
    user = Users(
        first_name="John", last_name="Doe", password="password", username="johndoe"
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@api.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    # Minimum set of data to create a user
    if not data or not all(
        key in data for key in ("first_name", "last_name", "username", "password")
    ):
        return jsonify({"error": "Missing values for creating a user"}), 400

    # Validate role
    valid_roles = [role.value for role in Roles]
    if data["role"] not in valid_roles:
        return jsonify({"error": "Invalid role"}), 400

    role = Roles(data["role"])

    existing_user = Users.query.filter_by(username=data["username"]).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 409

    new_user = Users(
        username=data["username"],
        password=data["password"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        role=role,
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201


@api.route("/users/<int:user_id>", methods=["GET"])
def get_user_information(user_id):
    user = db.session.get(Users, user_id)
    if user:
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({"error": "User not found"}), 404


@api.route("users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = db.session.get(Users, user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        return jsonify({"error": "User not found"}), 404
