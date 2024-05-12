## Local Usage

1. Install the dependencies for the Poetry server:
   ```shell
   poetry install --no-root
   ```
2. Start the Poetry server:
   ```shell
   poetry run flask --app brewbucks run --host 0.0.0.0 --port 8080
   ```

## Docker Image
- Flask runs on port 80


## API Information

### Production Endpoint
1. `GET` `/api/v1/health`: 
- returns status code 200 when healthy

### Testing Endpoints (will be removed later)
1. `GET` `/api/v1/users_test`: 
- creates a `John Doe` user with username `johndoe` and password `password`
-  Returns 201 along with user created info.

### Proposed Endpoints

1. `POST` `/api/v1/users`:
-  Create new users. 
- Follow the User Model.
- return code 201 if successful. 
- Error codes 40x and 50x based on error.

2. `POST` `api/v1/users/login`:
- Login user.

3. `GET` `api/v1/users/{user_id}`:
- Get user information.

4. `PUT` `api/v1/users/{user_id}`:
- Update user information.

5. `DELETE` `api/v1/users/{user_id}`:
- Delete user.

6. `GET` `api/v1/users/{user_id}/orders`:
- Get all orders for a user.

7. `POST` `api/v1/users/{user_id}/orders`:
- Create a new order for a user.

8. `GET` `api/v1/users/{user_id}/orders/{order_id}`:
- Get order information.

9. `PUT` `api/v1/users/{user_id}/orders/{order_id}`:
- Update order information.

10. `GET` `api/v1/users/{user_id}/orders/{order_id}/items`:
- Get all items in an order.

11. `POST` `api/v1/users/{user_id}/orders/{order_id}/items`:
- Add an item to an order.

12. `POST` `api/v1/users/{user_id}/orders/{order_id}/payment`:
- Add payment to an order.

13. `GET` `api/v1/users/{user_id}/orders/{order_id}/payment`:
- Get payment information for an order.