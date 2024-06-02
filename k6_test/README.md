# macOS
brew install k6

# Windows (Using Chocolatey)
choco install k6

# Linux
sudo apt install k6



k6 run  sign_up_and_delete_user.js
k6 run  get_user_info.js
k6 run  create_menu_item.js
k6 run  get_menu_item.js
k6 run  create_order.js

1. User Sign-Up and Deletion (sign_up_and_delete_user.js)
Total Requests: 7116
Successful Requests: 100.00%
Average HTTP Request Duration: 10.42ms
HTTP Request Failure Rate: 0.00%
2. Get User Info (get_user_info.js)
Total Requests: 3605
Successful Requests: 100.00%
Average HTTP Request Duration: 6.62ms
HTTP Request Failure Rate: 0.00%
3. Create Menu Item (create_menu_item.js)
Total Requests: 3606
Successful Requests: 100.00%
Average HTTP Request Duration: 7.34ms
HTTP Request Failure Rate: 0.00%
4. Get Menu Items (get_menu_item.js)
Total Requests: 1260
Successful Requests: 78.05%
Average HTTP Request Duration: 1.89s
HTTP Request Failure Rate: 0.00%
5. Create Order (create_order.js)
Total Requests: 3584
Successful Requests: 100.00%
Average HTTP Request Duration: 13.4ms
HTTP Request Failure Rate: 0.00%