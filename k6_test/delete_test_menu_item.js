import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
    vus: 1, 
    duration: '120m', 
};

export default function () {
    
    const userId = 1;

    
    let getItemsRes = http.get('http://brewbucks-485861802.us-east-1.elb.amazonaws.com/api/v1/menu_items', {
        headers: { 'Content-Type': 'application/json' },
    });

    check(getItemsRes, {
        'items retrieval status is 200': (r) => r.status === 200,
    });

    let items = getItemsRes.json();
    let itemsToDelete = items.slice(5); 

    
    itemsToDelete.forEach(item => {
        let deleteData = JSON.stringify({
            user_id: userId,
            item_id: item.item_id,
        });

        
        deleteItem(deleteData, item.name);
    });
}

function deleteItem(deleteData, itemName) {
    let deleteRes = http.del('http://brewbucks-485861802.us-east-1.elb.amazonaws.com/api/v1/menu_items', deleteData, {
        headers: { 'Content-Type': 'application/json' },
    });

    
    console.log(`Delete response for ${itemName}: ${deleteRes.status} ${deleteRes.body}`);

    check(deleteRes, {
        [`item deletion status for ${itemName} is 200`]: (r) => r.status === 200,
    });

   
}
