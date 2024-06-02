from datetime import datetime, timezone
import pytest
from brewbucks import create_app
from brewbucks.models import db
from brewbucks.models.users import Users, Roles
from brewbucks.models.order import Orders, OrderStatus
from brewbucks.models.payments import PaymentStatus
from brewbucks.models.menu_item import MenuItems
from brewbucks.models.order_items import OrderItems
from brewbucks.models.rewards import Rewards
from flask import jsonify

from enum import Enum



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
def sample_orders(app, sample_user):
    with app.app_context():
        orders_data = [
            {"user_id": sample_user.user_id, "order_status": OrderStatus.Processing.name, "payment_status": PaymentStatus.Pending, "total": 10.0},
            {"user_id": sample_user.user_id, "order_status": OrderStatus.Making.name, "payment_status": PaymentStatus.Pending, "total": 20.0},
            {"user_id": sample_user.user_id, "order_status": OrderStatus.Completed.name, "payment_status": PaymentStatus.Paid, "total": 30.0},
            {"user_id": sample_user.user_id, "order_status": OrderStatus.Making.name, "payment_status": PaymentStatus.Pending, "total": 40.0}
        ]
        orders = []
        for order_data in orders_data:
            new_order = Orders(
                user_id=order_data["user_id"],
                order_status=OrderStatus[order_data["order_status"]],
                payment_status=order_data["payment_status"],
                total=order_data["total"],
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            db.session.add(new_order)
            db.session.commit()
            orders.append(new_order)
        yield orders
        # Cleanup
        for order in orders:
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


def test_create_menu(client):
    response = client.post("/api/v1/test_menuitems")
    assert response.status_code == 201


def test_create_menu_item(client, sample_user):
    # 首先创建测试菜单项
    test_create_menu(client)

    # 新的菜单项数据
    item_data = {
        "user_id": sample_user.user_id,
        "name": "Flat White",
        "description": "Smooth and velvety coffee",
        "price": 3.5,
        "orderable": True
    }
    
    # 创建新的菜单项
    response = client.post("/api/v1/menu_items", json=item_data)
    assert response.status_code == 201
    assert response.json["name"] == item_data["name"]
    assert response.json["description"] == item_data["description"]
    assert response.json["price"] == item_data["price"]
    assert response.json["orderable"] is item_data["orderable"]

    # 验证新的菜单项是否确实被创建
    response = client.get("/api/v1/menu_items")
    assert response.status_code == 200
    menu_items = response.json
    assert any(item["name"] == "Flat White" and item["description"] == "Smooth and velvety coffee" for item in menu_items)


def test_get_menu_items(client):
    
    test_create_menu(client)

    
    response = client.get("/api/v1/menu_items")
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_update_menu_item(client, sample_user):
    # 首先创建测试菜单项
    test_create_menu(client)

    # 获取菜单项，以便获取要更新的项目ID
    response = client.get("/api/v1/menu_items")
    assert response.status_code == 200
    menu_items = response.json

    # 假设要更新 Espresso 项目
    espresso_item = next(item for item in menu_items if item["name"] == "Espresso")
    update_data = {
        "user_id": sample_user.user_id,
        "name": "Updated Espresso",
        "description": "Strong and bold",
        "price": 3.0,
        "orderable": True
    }

    # 进行更新操作
    response = client.put(f"/api/v1/menu_items/{espresso_item['item_id']}", json=update_data)
    assert response.status_code == 200
    assert response.json["name"] == "Updated Espresso"
    assert response.json["description"] == "Strong and bold"
    assert response.json["price"] == 3.0
    assert response.json["orderable"] is True

    # 验证项目确实被更新
    response = client.get(f"/api/v1/menu_items/{espresso_item['item_id']}")
    assert response.status_code == 200
    updated_item = response.json
    assert updated_item["name"] == "Updated Espresso"
    assert updated_item["description"] == "Strong and bold"
    assert updated_item["price"] == 3.0
    assert updated_item["orderable"] is True


def test_delete_menu_item(client, sample_user):
    
    test_create_menu(client)

    
    response = client.get("/api/v1/menu_items")
    assert response.status_code == 200
    menu_items = response.json

    
    latte_item = next(item for item in menu_items if item["name"] == "Latte")
    delete_data = {
        "user_id": sample_user.user_id,
        "item_id": latte_item["item_id"]
    }

    
    response = client.delete("/api/v1/menu_items", json=delete_data)
    assert response.status_code == 200
    assert response.json["message"] == "Menu item deleted successfully"

   
    response = client.get("/api/v1/menu_items")
    assert response.status_code == 200
    menu_items = response.json
    assert not any(item["item_id"] == latte_item["item_id"] for item in menu_items)


def test_create_order_success(client, sample_user):
    
    response = client.post("/api/v1/test_menuitems")
    assert response.status_code == 201

   
    response = client.get("/api/v1/menu_items")
    assert response.status_code == 200
    menu_items = response.json

    
    latte_item = next(item for item in menu_items if item["name"] == "Latte")
    mocha_item = next(item for item in menu_items if item["name"] == "Mocha")

   
    order_data = {
        "user_id": sample_user.user_id,
        "order_items": [
            {"item_id": latte_item["item_id"], "quantity": 2},
            {"item_id": mocha_item["item_id"], "quantity": 3}
        ],
        "rewards_added": 5
    }
    
    print(f"Order data being sent: {order_data}")

    response = client.post("/api/v1/users/orders", json=order_data)
    print(f"Response status code: {response.status_code}")
    print(f"Response data: {response.json}")

    assert response.status_code == 201
    expected_total = 2 * latte_item["price"] + 3 * mocha_item["price"]
    assert response.json["order"]["total"] == expected_total


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


def test_get_order_items(client, sample_user):
    
    test_create_menu(client)

    
    response = client.get("/api/v1/menu_items")
    assert response.status_code == 200
    menu_items = response.json

   
    latte_item = next(item for item in menu_items if item["name"] == "Latte")

    
    order_data = {
        "user_id": sample_user.user_id,
        "order_items": [
            {"item_id": latte_item["item_id"], "quantity": 1}
        ],
        "rewards_added": 5
    }

    
    response = client.post("/api/v1/users/orders", json=order_data)
    assert response.status_code == 201
    created_order = response.json["order"]

   
    response = client.get(f"/api/v1/users/{sample_user.user_id}/orders/{created_order['order_id']}/items")
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert any(item["menu_item_id"] == latte_item["item_id"] for item in response.json)


def test_update_order_item(client, sample_user):
   
    test_create_menu(client)

   
    response = client.get("/api/v1/menu_items")
    assert response.status_code == 200
    menu_items = response.json

    
    latte_item = next(item for item in menu_items if item["name"] == "Latte")

    
    order_data = {
        "user_id": sample_user.user_id,
        "order_items": [
            {"item_id": latte_item["item_id"], "quantity": 3}
        ],
        "rewards_added": 5
    }

    
    response = client.post("/api/v1/users/orders", json=order_data)
    assert response.status_code == 201
    created_order = response.json["order"]

   
    response = client.get(f"/api/v1/users/{sample_user.user_id}/orders/{created_order['order_id']}/items")
    assert response.status_code == 200
    order_items = response.json
    order_item_id = order_items[0]["order_item_id"]

    
    update_data = {
        "quantity": 5
    }
    response = client.put(f"/api/v1/users/{sample_user.user_id}/orders/{created_order['order_id']}/items/{order_item_id}", json=update_data)
    assert response.status_code == 200
    assert response.json["quantity"] == update_data["quantity"]


def test_delete_order_item(client, sample_user):
   
    test_create_menu(client)

   
    response = client.get("/api/v1/menu_items")
    assert response.status_code == 200
    menu_items = response.json

   
    latte_item = next(item for item in menu_items if item["name"] == "Latte")


    order_data = {
        "user_id": sample_user.user_id,
        "order_items": [
            {"item_id": latte_item["item_id"], "quantity": 1}
        ],
        "rewards_added": 5
    }

  
    response = client.post("/api/v1/users/orders", json=order_data)
    assert response.status_code == 201
    created_order = response.json["order"]

   
    response = client.get(f"/api/v1/users/{sample_user.user_id}/orders/{created_order['order_id']}/items")
    assert response.status_code == 200
    order_items = response.json
    order_item_id = order_items[0]["order_item_id"]

   
    response = client.delete(f"/api/v1/users/{sample_user.user_id}/orders/{created_order['order_id']}/items/{order_item_id}")
    assert response.status_code == 200
    assert response.json["message"] == "Order item deleted successfully"


def test_get_active_orders(client, sample_user, sample_orders):
  
    response = client.get("/api/v1/orders/active", json={"user_id": sample_user.user_id})
    assert response.status_code == 200
    active_orders = response.json
    assert isinstance(active_orders, list)
    
   
    for order in active_orders:
        print(f"Order ID: {order['order_id']}, Status: {order['order_status']}")

    assert len(active_orders) == 3  
    for order in active_orders:
        assert order["order_status"] in ["Processing", "Making"]
        assert order["user_id"] == sample_user.user_id


def test_get_finished_orders(client, sample_user, sample_orders):
    response = client.get(f"/api/v1/orders/finished?user_id={sample_user.user_id}")
    assert response.status_code == 200
    finished_orders = response.json
    assert isinstance(finished_orders, list)
    assert len(finished_orders) == 1



def test_get_making_orders(client, sample_user, sample_orders):
    response = client.get(f"/api/v1/orders/making?user_id={sample_user.user_id}")
    assert response.status_code == 200
    making_orders = response.json
    assert isinstance(making_orders, list)
    assert len(making_orders) == 2



def test_get_making_orders_all(client, sample_orders):
    
    response = client.get("/api/v1/orders/display_screen")
    assert response.status_code == 200
    making_orders_all = response.json
    assert isinstance(making_orders_all, list)
    assert len(making_orders_all) == 2  
    for order in making_orders_all:
        assert order["order_status"] == "Making"


def test_create_and_get_rewards(client, sample_user):
    reward_data = {
        "customer_id": sample_user.user_id,
        "total_points": 300
    }
    new_reward = Rewards(
        customer_id=reward_data["customer_id"],
        total_points=reward_data["total_points"],
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    with client.application.app_context():
        db.session.add(new_reward)
        db.session.commit()

    with client.application.app_context():
        reward = Rewards.query.filter_by(customer_id=sample_user.user_id).first()
        assert reward is not None
        assert reward.total_points == 300

    response = client.get(f"/api/v1/users/rewards?user_id={sample_user.user_id}")
    assert response.status_code == 200
    response_data = response.json
    assert "User points" in response_data
    assert "Rewards details" in response_data
    assert len(response_data["User points"]) > 0
    assert response_data["User points"][0] == 300

