import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
    stages: [
        { duration: '1m', target: 20 }, // Ramp-up to 20 users over 1 minute
        { duration: '2m', target: 20 }, // Stay at 20 users for 2 minutes
        { duration: '1m', target: 0 },  // Ramp-down to 0 users over 1 minute
    ],
};

export default function () {
    let orderData = JSON.stringify({
        user_id: 1,
        order_items: [
            { item_id: 1, quantity: 2 },
            { item_id: 2, quantity: 1 },
        ],
        rewards_added: 5,
    });

    let createOrderRes = http.post('http://localhost:8080/api/v1/users/orders', orderData, {
        headers: { 'Content-Type': 'application/json' },
    });

    check(createOrderRes, {
        'order creation status is 201': (r) => r.status === 201,
    });

    sleep(1);
}
