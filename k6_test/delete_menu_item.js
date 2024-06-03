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
    let res = http.get('http://brewbucks-485861802.us-east-1.elb.amazonaws.com/api/v1/menu_items', {
        headers: { 'Content-Type': 'application/json' },
    });

    latte_item = next(item for item in menu_items)
    delete_data = {
        "user_id": 1,
        "item_id": latte_item["item_id"]
    }

    let itemData = JSON.stringify({
        user_id: 1,
        item_id: 9
    });



    let delItemRes = http.del('http://brewbucks-485861802.us-east-1.elb.amazonaws.com/api/v1/menu_items', itemData, {
        headers: { 'Content-Type': 'application/json' },
    });

    check(delItemRes, {
        'item deletion status is 201': (r) => r.status === 201,
    });

    let itemId = delItemRes.json().item_id;

    sleep(1);
}
