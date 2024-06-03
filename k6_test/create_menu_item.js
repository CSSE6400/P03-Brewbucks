import http from 'k6/http';
import { check, sleep } from 'k6';

export function uuidv4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = (Math.random() * 16) | 0,
            v = c == 'x' ? r : (r & 0x3) | 0x8;
        return v.toString(16);
    });
}


export const options = {
    stages: [
        { duration: '1m', target: 20 },
        { duration: '2m', target: 20 },
        { duration: '1m', target: 0 },
    ],
};

export default function () {
    let itemData = JSON.stringify({
        user_id: 1,
        name: `Item_${uuidv4()}`,
        description: 'Test item',
        price: 10.0,
        orderable: true,
    });

    let createItemRes = http.post('http://brewbucks-485861802.us-east-1.elb.amazonaws.com/api/v1/menu_items', itemData, {
        headers: { 'Content-Type': 'application/json' },
    });

    check(createItemRes, {
        'item creation status is 201': (r) => r.status === 201,
    });

    let itemId = createItemRes.json().item_id;


    sleep(1);
}
