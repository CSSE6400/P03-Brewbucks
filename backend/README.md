## Local Usage

1. Install the dependencies for the Poetry server:
   ```shell
   poetry install --no-root
   ```
2. Start the Poetry server:
   ```shell
   poetry run flask --app brewbucks run --host 0.0.0.0 --port 8080 --debug
   ```

## Docker Image
- Flask runs on port 80


## API Information

### Production Endpoint
1. `GET` `/api/v1/health`: 
- returns status code 200 when healthy

1. `POST` `/api/v1/users`: (Done)
-  Create new users. 
- Follow the User Model.
- return code 201 if successful. 
- Error codes 40x and 50x based on error.

- example test:
{
    "username" : "karthikeya_v"
    ,"password" : "karthik123"
    ,"role":"employee"
    ,"first_name":"karthikeya"
    ,"last_name":"v"
}

2. `POST` `api/v1/users/login`: (done)
- Login user.

example test:
{
    "username" : "karthikeya_v"
    ,"password" : "karthik123"
}

3. `GET` `api/v1/users/{user_id}`:(done)
- Get user information for a specific user using user_id.

example : get api/v1/users/1

4. `PUT` `api/v1/users/:(done)
- Update user information.
examples:
    "user_id" :"19"
    "username" : "karthikeya_v"
    ,"password" : "karthik123"
    ,"role":"employee"
    ,"first_name":"karthikeya"
    ,"last_name":"v"

5. `DELETE` `api/v1/users/{user_id}`:(Done)
- Delete user.
example Delele api/v1/users/19

6. `GET` `api/v1/users/{user_id}/orders`:(Done)
- Get all orders for a user.
Get api/v1/users/19/orders

7. `POST` `api/v1/users/orders`:(Done)
- Create a new order for a user.
    {
    "user_id":"19",
    "total" : "59"
    ,"payment_status" : 1
    ,"order_status":2
    ,"rewards_added":10
}

# Route to create a new order item based on menu item id
@api.route('/order_items', methods=['POST'])

creates order_items based on the menu_item_id and order provided

8. `GET` `api/v1/users/{user_id}/orders/{order_id}`:(Done)
- Get order information.
    example: api/v1/users/19/orders/1

9. `PUT` `api/v1/users/{user_id}/orders/{order_id}`:
- Update order information.
{
    "user_id":"19",
    "total" : "59"
    ,"payment_status" : 1
    ,"order_status":2
    ,"rewards_added":10
}

10. `GET` `api/v1/users/{user_id}/orders/{order_id}/items`:
- Get all items in an order.
api/v1/users/{user_id}/orders/{order_id}/items`

11. `POST` `api/v1/users/{user_id}/orders/{order_id}/items`:
- Add an item to an order.


12. `POST` `api/v1/users/{user_id}/orders/{order_id}/payment`:
- Add payment to an order.

13. `GET` `api/v1/users/{user_id}/orders/{order_id}/payment`:

- Get payment information for an order.

14. 'GET' '/menu_items':
- Retrieves all menu items.

15. GET /menu_items/<int:item_id>:
- Retrieves a specific menu item by item_id.

16. POST /menu_items:
- Creates a new menu item. Expects JSON data with name,   description, and price. Optionally, orderable can be provided (defaults to True).

17. PUT /menu_items/<int:item_id>:
- Updates an existing menu item by item_id. Expects JSON data with any fields to update (name, description, price, orderable).

18. DELETE /menu_items/<int:item_id>:
- Deletes a menu item by item_id if the user is a employee

###API Routes with Request Bodies
##User Routes
1. Create User
POST /api/v1/users
Request Body:
{
    "first_name": "Jane",
    "last_name": "Smith",
    "password": "mypassword",
    "username": "janesmith",
    "role": "Customer"
}
updates: made username unique
2. Login
POST /api/v1/users/login
Request Body:
{
    "username": "janesmith",
    "password": "mypassword"
}
3. Update User Info
PUT /api/v1/users
Request Body:
{
    "first_name": "Jane",
    "last_name": "Doe",
    "password": "newpassword",
    "username": "janedoe",
    "role": "Admin"
}
Order Routes
0. route to get all finished orders
@api.route('/orders/finished', methods=['GET'])

1. show all active orders
GET /api/v1/users/active

2. Create User Order
POST /api/v1/users/orders
Request Body:
{
    "user_id": 1,
    "total": 200.00,
    "payment_status": "Pending",
    "order_status": "Processing",
    "rewards_added": 50
}
3. Update Order
PUT /api/v1/users/orders
Request Body:
{
    "user_id": 1,
    "order_id": 123,
    "payment_status": 1,
    "order_status": 2,
    "rewards_added": 50,
    "total": 250.00
}
4. Delete Order
DELETE /api/v1/users/orders
Request Body:
{
    "order_id": 123
}
Menu Item Routes

0. added a route to create test use-cases of menu_items
POST /api/v1/test_menuitems

1. Create Menu Item
POST /api/v1/menu_items
Request Body:
{
    "user_id": 1,
    "name": "Latte",
    "description": "A delicious coffee drink",
    "price": 4.50,
    "orderable": true
}
2. Update Menu Item
PUT /api/v1/menu_items/<int:item_id>
Request Body:
{
    "user_id": 1,
    "name": "Latte",
    "description": "A delicious coffee drink",
    "price": 4.75,
    "orderable": true
}
3. Delete Menu Item
DELETE /api/v1/menu_items
Request Body:
{
    "user_id": 1,
    "item_id": 12
}
Order Item Routes
1. Create Order Item
POST /api/v1/order_items
Request Body:
{
    "user_id": 1,
    "order_id": 12,
    "menu_item_id": 1,
    "quantity": 2
}
2. Update Order Item
PUT /api/v1/users/<int:user_id>/orders/<int:order_id>/items/<int:order_item_id>
Request Body:
{
    "menu_item_id": 2,
    "quantity": 3
}
3. Delete Order Item
DELETE /api/v1/users/<int:user_id>/orders/<int:order_id>/items/<int:order_item_id>
Request Body:
{
    "user_id": 1,
    "order_id": 12,
    "order_item_id": 4
}
