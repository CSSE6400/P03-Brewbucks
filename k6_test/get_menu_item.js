import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
    stages: [
        { duration: '1m', target: 45 },
        { duration: '2m', target: 75 },
        { duration: '1m', target: 0 },
    ],
};

export default function () {
    let res = http.get('http://brewbucks-485861802.us-east-1.elb.amazonaws.com/api/v1/menu_items', {
        headers: { 'Content-Type': 'application/json' },
    });

    check(res, {
        'status is 200': (r) => r.status === 200,
        'response time is < 750ms': (r) => r.timings.duration < 750,
    });

    sleep(1);
}
