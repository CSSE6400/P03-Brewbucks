import pytest
from brewbucks import create_app
from brewbucks.models.users import db, Users
from flask import json, jsonify


@pytest.fixture
def app():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def sample_user(app):
    with app.app_context():
        user = Users(
            username="sampleuser",
            password="password",
            first_name="Sample",
            last_name="User",
        )
        db.session.add(user)
        db.session.commit()
        yield user
        # Before cleanup, check if the user still exists, needed since some of the tests might delete the sample user.
        exists = (
            db.session.query(Users.user_id).filter_by(user_id=user.user_id).scalar()
            is not None
        )
        if exists:
            db.session.delete(user)
            db.session.commit()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


def test_health(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json == {"status": "Healthy"}


def test_create_test_user(client):
    response = client.post("/api/v1/users_test")
    assert response.status_code == 201
    assert "johndoe" in response.json["username"]


def test_create_user(client):
    user_data = {
        "username": "janedddoe",
        "password": "password",
        "first_name": "Jane",
        "last_name": "Doe",
        "role": "customer",
    }
    response = client.post("/api/v1/users", json=user_data)
    assert response.status_code == 201
    assert response.json["username"] == user_data["username"]
    assert response.json["first_name"] == user_data["first_name"]
    assert response.json["last_name"] == user_data["last_name"]
    assert response.json["role"] == user_data["role"]


def test_get_user_information(client, sample_user):
    response = client.get(f"/api/v1/users/{sample_user.user_id}")
    assert response.status_code == 200
    assert response.json["username"] == "sampleuser"


def test_delete_non_existing_user(client):
    response = client.delete("/api/v1/users/9999")  # Assuming 9999 is a non-existing ID
    assert response.status_code == 404
    assert response.json["error"] == "User not found"


def test_delete_sample_user(client, sample_user):
    user = db.session.get(Users, sample_user.user_id)
    print(user.user_id)
    response = client.delete(f"/api/v1/users/{sample_user.user_id}")
    assert response.status_code == 200
    assert response.json["message"] == "User deleted successfully"
