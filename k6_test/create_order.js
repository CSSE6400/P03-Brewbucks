import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
    stages: [
        { duration: '2m', target: 1000 }, // Ramp-up to 2000 users over 1 minute
        { duration: '2m', target: 2500 }, // Stay at 2500 users for 2 minutes
        { duration: '2m', target: 0 },  // Ramp-down to 0 users over 2 minute
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

    let createOrderRes = http.post('http://brewbucks-485861802.us-east-1.elb.amazonaws.com/api/v1/users/orders', orderData, {
        headers: { 'Content-Type': 'application/json' },
    });

    check(createOrderRes, {
        'order creation status is 201': (r) => r.status === 201,
    });

    sleep(1);
}
