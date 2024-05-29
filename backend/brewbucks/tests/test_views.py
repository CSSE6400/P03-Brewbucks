import pytest
from brewbucks import create_app
from brewbucks.models import db
from brewbucks.models.users import Users, Roles
from brewbucks.models.order import Orders, OrderStatus
from brewbucks.models.payments import PaymentStatus
from brewbucks.models.menu_item import MenuItems
from brewbucks.models.order_items import OrderItems
from flask import jsonify


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
            role=Roles.Employee,
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
def sample_menu_item(app):
    with app.app_context():
        item = MenuItems(
            name="Latte",
            description="A hot cup of latte",
            price=5.0,
            orderable=True
        )
        db.session.add(item)
        db.session.commit()
        yield item
        exists = (
            db.session.query(MenuItems.item_id).filter_by(item_id=item.item_id).scalar()
            is not None
        )
        if exists:
            db.session.delete(item)
            db.session.commit()


@pytest.fixture
def sample_order(app, sample_user):
    with app.app_context():
        order = Orders(
            user_id=sample_user.user_id,
            total=15.0,
            payment_status=PaymentStatus.Pending,
            order_status=OrderStatus.Processing
        )
        db.session.add(order)
        db.session.commit()
        yield order
        exists = (
            db.session.query(Orders.order_id).filter_by(order_id=order.order_id).scalar()
            is not None
        )
        if exists:
            db.session.delete(order)
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


def test_update_user_info(client, sample_user):
    update_data = {
        "user_id": sample_user.user_id,
        "first_name": "Updated",
        "last_name": "User"
    }
    response = client.put('/api/v1/users', json=update_data)
    assert response.status_code == 200
    assert response.json["first_name"] == "Updated"
    assert response.json["last_name"] == "User"


def test_delete_sample_user(client, sample_user):
    user = db.session.get(Users, sample_user.user_id)
    print(user.user_id)
    response = client.delete(f"/api/v1/users/{sample_user.user_id}")
    assert response.status_code == 200
    assert response.json["message"] == "User deleted successfully"


def test_delete_non_existing_user(client):
    response = client.delete("/api/v1/users/9999") # Assuming 9999 is a non-existing ID
    assert response.status_code == 404
    assert response.json["error"] == "User not found"


def test_user_login(client, sample_user):
    login_data = {
        "username": "sampleuser",
        "password": "password"
    }
    response = client.post("/api/v1/users/login", json=login_data)
    assert response.status_code == 200

    invalid_login_data = {
        "username": "sampleuser",
        "password": "wrongpassword"
    }
    response = client.post("/api/v1/users/login", json=invalid_login_data)
    assert response.status_code == 401


def test_create_menu_item(client, sample_user):
    item_data = {
        "user_id": sample_user.user_id,
        "name": "Espresso",
        "description": "Strong and bold",
        "price": 3.0,
        "orderable": True
    }
    response = client.post("/api/v1/menu_items", json=item_data)
    assert response.status_code == 201
    assert response.json["name"] == item_data["name"]


def test_get_menu_items(client, sample_menu_item):
    response = client.get("/api/v1/menu_items")
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert any(item["name"] == sample_menu_item.name for item in response.json)


def test_update_menu_item(client, sample_user, sample_menu_item):
    update_data = {
        "user_id": sample_user.user_id,
        "name": "Updated Espresso",
        "description": "Strong and bold",
        "price": 3.0,
        "orderable": True
    }
    response = client.put(f"/api/v1/menu_items/{sample_menu_item.item_id}", json=update_data)
    assert response.status_code == 200


def test_delete_menu_item(client, sample_menu_item, sample_user):
    delete_data = {
        "user_id": sample_user.user_id,
        "item_id": sample_menu_item.item_id
    }
    response = client.delete("/api/v1/menu_items", json=delete_data)
    assert response.status_code == 200
 

def test_create_order_success(client, sample_user):
    order_data = {
        "user_id": sample_user.user_id,
        "total": 10.0,
        "payment_status": PaymentStatus.Pending.name,  
        "order_status": OrderStatus.Processing.name,  
        "rewards_added": 5
    }
    response = client.post("/api/v1/users/orders", json=order_data)
    assert response.status_code == 201


def test_create_order_invalid_user(client):
    order_data = {
        "user_id": 9999,  # Assuming 9999 is a non-existing user ID
        "total": 10.0,
        "payment_status": PaymentStatus.Pending.name,
        "order_status": OrderStatus.Processing.name,
        "rewards_added": 5
    }
    response = client.post("/api/v1/users/orders", json=order_data)
    assert response.status_code == 404
    assert response.json["error"] == "User not found"


def test_get_order_items(client, sample_user, sample_order, sample_menu_item):
    item_data = {
        "user_id": sample_user.user_id,
        "order_id": sample_order.order_id,
        "menu_item_id": sample_menu_item.item_id,
        "quantity": 1
    }
    client.post("/api/v1/order_items", json=item_data)
    response = client.get(f"/api/v1/users/{sample_user.user_id}/orders/{sample_order.order_id}/items")
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert any(item["menu_item_id"] == sample_menu_item.item_id for item in response.json)


def test_add_order_item(client, sample_user, sample_order, sample_menu_item):
    item_data = {
        "user_id": sample_user.user_id,
        "order_id": sample_order.order_id,
        "menu_item_id": sample_menu_item.item_id,
        "quantity": 2
    }
    response = client.post("/api/v1/order_items", json=item_data)
    assert response.status_code == 201
    assert response.json["menu_item_id"] == sample_menu_item.item_id
    assert response.json["quantity"] == item_data["quantity"]


def test_update_order_item(client, sample_user, sample_order, sample_menu_item):
    item_data = {
        "user_id": sample_user.user_id,
        "order_id": sample_order.order_id,
        "menu_item_id": sample_menu_item.item_id,
        "quantity": 1
    }
    post_response = client.post("/api/v1/order_items", json=item_data)
    order_item_id = post_response.json["order_item_id"]
    update_data = {
        "quantity": 3
    }
    response = client.put(f"/api/v1/users/{sample_user.user_id}/orders/{sample_order.order_id}/items/{order_item_id}", json=update_data)
    assert response.status_code == 200
    assert response.json["quantity"] == update_data["quantity"]


def test_delete_order_item(client, sample_user, sample_order, sample_menu_item):
    item_data = {
        "user_id": sample_user.user_id,
        "order_id": sample_order.order_id,
        "menu_item_id": sample_menu_item.item_id,
        "quantity": 1
    }
    post_response = client.post("/api/v1/order_items", json=item_data)
    order_item_id = post_response.json["order_item_id"]
    response = client.delete(f"/api/v1/users/{sample_user.user_id}/orders/{sample_order.order_id}/items/{order_item_id}")
    assert response.status_code == 200
    assert response.json["message"] == "Order item deleted successfully"


