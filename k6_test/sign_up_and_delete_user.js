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
    let userData = JSON.stringify({
        username: `user_${uuidv4()}`,
        password: 'password',
        first_name: 'Test',
        last_name: 'User',
        role: 'customer',
    });

    let createUserRes = http.post('http://brewbucks-485861802.us-east-1.elb.amazonaws.com/api/v1/users', userData, {
        headers: { 'Content-Type': 'application/json' },
    });

    check(createUserRes, {
        'user creation status is 201': (r) => r.status === 201,
    });

    let userId = createUserRes.json().user_id;

    let deleteUserRes = http.del(`http://brewbucks-485861802.us-east-1.elb.amazonaws.com/api/v1/users/${userId}`);

    check(deleteUserRes, {
        'user deletion status is 200': (r) => r.status === 200,
    });

    sleep(1);
}
