import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
    stages: [
        { duration: '1m', target: 1000 },
        { duration: '2m', target: 2000 },
        { duration: '1m', target: 0 },
    ],
};

export default function () {
    let res = http.get('http://brewbucks-485861802.us-east-1.elb.amazonaws.com/api/v1/users/1', {
        headers: { 'Content-Type': 'application/json' },
    });

    check(res, {
        'status is 200': (r) => r.status === 200,
        'response time is < 1000ms': (r) => r.timings.duration < 1000,
    });

    sleep(1);
}
