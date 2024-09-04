async function _get_ai_pokemon(data) {
    const response = await fetch('http://localhost:8000/get_ai_pokemon', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });

    return await response.json();
}

async function _get_user_pokemon(data) {
    const response = await fetch('http://localhost:8000/get_user_pokemon', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });

    return await response.json();
}

async function _ai_turn(data) {
    const response = await fetch('http://localhost:8000/ai_turn', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });

    return await response.json();
}

// async function _ai_turn() {
//     const response = await fetch('http://localhost:8000/ai_turn', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({"hi": "bye"}),
//     });

//     return await response.json();
// }

async function _user_turn(data) {
    const response = await fetch('http://localhost:8000/user_turn', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });

    return await response.json();
}

// Usage

// async function fuck(){
//     _get_ai_pokemon({pokemon_description: 'An ice cream cone'}).then(result => console.log(result));
// }

async function get_ai_pokemon(){
    ai_pokemon = _get_ai_pokemon({img_path: '../../Downloads/profile-pic.jpg'}).then(result => console.log(result));
    return ai_pokemon
}


async function get_user_pokemon(){
    user_pokemon = _get_user_pokemon({img_path: '../../Downloads/profile-pic.jpg'}).then(result => console.log(result));
    return user_pokemon
}


async function ai_turn(){
    output = _ai_turn({data: "data"}).then(result => console.log(result));
    // return attack, insult
    return output
}


async function user_turn(){
    insult = _user_turn({"user_attack": "kill"}).then(result => console.log(result));
    return insult
}
