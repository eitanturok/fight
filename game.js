const FPS = 6;

let ai_picture_path = "";
let your_picture_path = "";

let ai_attack_hit_frame = -1000;
let your_attack_hit_frame = -1000;
let ai_attack_miss_frame = -1000;
let your_attack_miss_frame = -1000;

let your_hp = 100;
let ai_hp = 100;

attacks = [];

attacks.push({
    title: "Chair Care",
    power: 10,
    accuracy: 0.9
});

attacks.push({
    title: "C2hair Care",
    power: 20,
    accuracy: 0.7
});

attacks.push({
    title: "3Chair Care",
    power: 30,
    accuracy: 0.5
});

ai_attacks = [];

ai_attacks.push({
    title: "Chair Care",
    power: 10,
    accuracy: 0.9
});

ai_attacks.push({
    title: "C2hair Care",
    power: 20,
    accuracy: 0.7
});

ai_attacks.push({
    title: "3Chair Care",
    power: 30,
    accuracy: 0.5
});

let game_started = false;

let current_frame = 0;

var backgroundImages = [];
for (var i = 0; i < 12; i++) {
    var img = new Image();
    img.src = 'assets/battle_backgrounds/frame_' + i + '_delay-0.2s.png';
    backgroundImages.push(img);
}

var explosionImages = [];
for (var i = 0; i < 6; i++) {
    var img = new Image();
    img.src = 'assets/explosions/frame_0' + i + '_delay-0.1s.png';
    explosionImages.push(img);
}

var yourImage = new Image();
var aiImage = new Image();
yourImage.src = 'assets/your.png';
aiImage.src = 'assets/ai.png';

const canvas = document.getElementById('game');
const context = canvas.getContext('2d');

const your_location_x_home = 185;
const your_location_y_home = 250;

const ai_location_x_home = 518;
const ai_location_y_home = 170;

const your_location_x = 100;
const your_location_y = 200;

const ai_location_x = 110;
const ai_location_y = 110;

const paddleWidth = 10, paddleHeight = 75, ballRadius = 7;
let upArrow = false, downArrow = false;

const paddle1 = { x: 0, y: canvas.height / 2 - paddleHeight / 2, width: paddleWidth, height: paddleHeight, dy: 5 };
const paddle2 = { x: canvas.width - paddleWidth, y: canvas.height / 2 - paddleHeight / 2, width: paddleWidth, height: paddleHeight, dy: 5 };
const ball = { x: canvas.width / 2, y: canvas.height / 2, radius: ballRadius, speed: 4, dx: 4, dy: 4 };

// function upload_player_image() {
//     var file = document.getElementById("player_image").files[0];
//     var reader = new FileReader();
//     reader.onload = function(e) {
//         yourImage.src = e.target.result;
//         console.log(e.target.result);
//     }
//     reader.readAsDataURL(file);

// }

document.getElementById('player_image').addEventListener('change', function(event) {
    const file = event.target.files[0];
    console.log(file);
    get_your({img_path: file["name"]}).then(result => {
        console.log(result);

        document.getElementById("your_card").style.display = "flex";
        document.getElementById("your_name").innerText = result[0]["name"];
        document.getElementById("your_description").innerText = result[0]["description"];
        document.getElementById("your_hp").innerText = "HP: " + result[0]["hp"];
        document.getElementById("your_attacks").innerText = "Attacks: " + result[0]["attack1"]["name"] + ", " + result[0]["attack2"]["name"] + ", " + result[0]["attack3"]["name"];

        your_picture_path = result[1];

        yourImage.src = result[1];

        attacks[0] = {
            title: result[0]["attack1"]["name"],
            power: result[0]["attack1"]["power"],
            accuracy: result[0]["attack1"]["accuracy"],
            description: result[0]["attack1"]["description"]
        }

        attacks[1] = {
            title: result[0]["attack2"]["name"],
            power: result[0]["attack2"]["power"],
            accuracy: result[0]["attack2"]["accuracy"],
            description: result[0]["attack2"]["description"]
        }

        attacks[2] = {
            title: result[0]["attack3"]["name"],
            power: result[0]["attack3"]["power"],
            accuracy: result[0]["attack3"]["accuracy"],
            description: result[0]["attack3"]["description"]
        }
    });


    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('player_image_show').src = e.target.result;
        }
        reader.readAsDataURL(file);
    }
});

async function get_your(data) {
    const response = await fetch('http://localhost:8000/get_user_pokemon', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });

    return response.json();
}

document.getElementById('ai_image').addEventListener('change', function(event) {
    const file = event.target.files[0];
    console.log(file);
    get_ai({img_path: file["name"]}).then(result => {
        console.log(result);

        document.getElementById("ai_card").style.display = "flex";
        document.getElementById("ai_name").innerText = result[0]["name"];
        document.getElementById("ai_description").innerText = result[0]["description"];
        document.getElementById("ai_hp").innerText = "HP: " + result[0]["hp"];
        document.getElementById("ai_attacks").innerText = "Attacks: " + result[0]["attack1"]["name"] + ", " + result[0]["attack2"]["name"] + ", " + result[0]["attack3"]["name"];

        ai_picture_path = result[1];

        aiImage.src = result[1];

        ai_attacks[0] = {
            title: result[0]["attack1"]["name"],
            power: result[0]["attack1"]["power"],
            accuracy: result[0]["attack1"]["accuracy"],
            description: result[0]["attack1"]["description"]
        }

        ai_attacks[1] = {
            title: result[0]["attack2"]["name"],
            power: result[0]["attack2"]["power"],
            accuracy: result[0]["attack2"]["accuracy"],
            description: result[0]["attack2"]["description"]
        }

        ai_attacks[2] = {
            title: result[0]["attack3"]["name"],
            power: result[0]["attack3"]["power"],
            accuracy: result[0]["attack3"]["accuracy"],
            description: result[0]["attack3"]["description"]
        }
    });



    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('ai_image_show').src = e.target.result;
        }
        reader.readAsDataURL(file);
    }
});

async function get_ai(data) {
    const response = await fetch('http://localhost:8000/get_ai_pokemon', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });

    return response.json();
}

document.getElementById('ai_image').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('ai_image_show').src = e.target.result;
        }
        reader.readAsDataURL(file);
    }
});

function use_attack(attack_number) {
    let power = attacks[attack_number]["power"];
    let accuracy = attacks[attack_number]["accuracy"];

    let attack_hit = false;

    if (Math.random() < accuracy) {
        ai_hp -= power;
        attack_hit = true;

        ai_attack_hit_frame = current_frame;
    } else {
        ai_attack_miss_frame = current_frame;
    }

    document.getElementById("trash_talk").innerText = "You chose " + attacks[attack_number]["title"] + " attack! " + attacks[attack_number]["description"];


    // TODO: Call AI attack with attack_hit
    _user_turn({user_attack: attacks[attack_number]["title"]}).then(result => {
        console.log(result);
        document.getElementById("trash_talk").innerText = result;
    });
    // const response_json = await _user_turn({user_attack: attacks[attack_number]["title"]});

    // document.getElementById("trash_talk").innerText = response_json;
}

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

function start_game(){
    game_started = true;

    // change the inner html of start_button to hide it
    document.getElementById('start_button').style.display = "none";

    document.getElementById('game_description').innerHTML = `<div class="card" style="width: 810px;">
                    <div class="card-body" id="trash_talk">
                        This is some text within a card body. This is some text within a card body.
                    </div>
                </div>

                <div class="row" style="margin: 0 auto; width: 800px;">
                    <div class="col">
                        <div class="card" style="width: 100%;">
                            <div class="card-body">
                                <h5 class="card-title">${attacks[0]["title"]}</h5>
                                <p class="card-text">
                                    Power: ${attacks[0]["power"]}
                                    Acc: ${attacks[0]["accuracy"]}
                                </p>
                                <button onclick="use_attack(0)" class="btn btn-danger">Use</button>
                            </div>
                        </div>
                    </div>
                    <div class="col">
                        <div class="card" style="width: 100%;">
                            <div class="card-body">
                                <h5 class="card-title">${attacks[1]["title"]}</h5>
                                <p class="card-text">
                                    Power: ${attacks[1]["power"]}
                                    Acc: ${attacks[1]["accuracy"]}
                                </p>
                                <button onclick="use_attack(1)" class="btn btn-danger">Use</button>
                            </div>
                        </div>
                    </div>
                    <div class="col">
                        <div class="card" style="width: 100%;">
                            <div class="card-body">
                                <h5 class="card-title">${attacks[2]["title"]}</h5>
                                <p class="card-text">
                                    Power: ${attacks[2]["power"]}
                                    Acc: ${attacks[2]["accuracy"]}
                                </p>
                                <button onclick="use_attack(2)" class="btn btn-danger">Use</button>
                            </div>
                        </div>
                    </div>
                </div>`;
}


function drawRect(x, y, w, h, color) {
    context.fillStyle = color;
    context.fillRect(x, y, w, h);
}

function drawCircle(x, y, r, color) {
    context.fillStyle = color;
    context.beginPath();
    context.arc(x, y, r, 0, Math.PI * 2, false);
    context.closePath();
    context.fill();
}

function update() {
    if (upArrow && paddle2.y > 0) paddle2.y -= paddle2.dy;
    if (downArrow && paddle2.y < canvas.height - paddle2.height) paddle2.y += paddle2.dy;

    ball.x += ball.dx;
    ball.y += ball.dy;

    if (ball.y + ball.radius > canvas.height || ball.y - ball.radius < 0) ball.dy *= -1;

    const paddle = (ball.x < canvas.width / 2) ? paddle1 : paddle2;

    if (ball.x + ball.radius > paddle.x && ball.y > paddle.y && ball.y < paddle.y + paddle.height) {
        ball.dx *= -1;
    }

    if (ball.x - ball.radius < 0 || ball.x + ball.radius > canvas.width) {
        ball.x = canvas.width / 2;
        ball.y = canvas.height / 2;
        ball.dx *= -1;
    }
}

function render() {
    context.drawImage(backgroundImages[current_frame % 12], 0, 0, canvas.width, canvas.height);

    if (ai_attack_hit_frame + 11 >= current_frame) {
        console.log(Math.floor((current_frame - ai_attack_hit_frame)/2));

        context.drawImage(explosionImages[Math.floor((current_frame - ai_attack_hit_frame)/2)], ai_location_x_home - 10, ai_location_y_home - 10, 130, 130);
    }

    context.drawImage(yourImage, your_location_x_home + (6 * (Math.floor(current_frame / 4) % 2)), your_location_y_home, 110, 110);
    context.drawImage(aiImage, ai_location_x_home +  + (6 * ((Math.floor((current_frame + 2) / 4) + 1) % 2)), ai_location_y_home, 110, 110);

    // drawRect(150-5, 165-5, 500+10, 120+10, '#423428');
    // drawRect(150, 165, 500, 120, '#5c4832');

    // drawRect(150-5, 165-5, 500+10, 120+10, '#423428');
    // drawRect(150, 165, 500, 120, '#5c4832');

    context.font = "12x PressStart2P";
    context.fillStyle = "#ffffff";
    context.fillText("AI HP: " + ai_hp, 510, 50);
    context.fillText("Your HP: " + your_hp, 80, 430);

    // drawRect(0, 0, canvas.width, canvas.height, '#000');
    // drawRect(paddle1.x, paddle1.y, paddle1.width, paddle1.height, '#fff');
    // drawRect(paddle2.x, paddle2.y, paddle2.width, paddle2.height, '#fff');
    // drawCircle(ball.x, ball.y, ball.radius, '#fff');
}

function render_menu() {
    context.drawImage(backgroundImages[current_frame % 12], 0, 0, canvas.width, canvas.height);
    // context.font = "50px Press Start 2P";
    // context.font = "48px 'Press Start 2P' system-ui";
    drawRect(150-5, 165-5, 500+10, 120+10, '#423428');
    drawRect(150, 165, 500, 120, '#5c4832');
    context.font = "28px PressStart2P";
    context.fillStyle = "#ffffff";
    context.fillText("Select Characters", 170, 210);
    context.fillText("and Press Play!", 196, 270);
}

function render_game_over(ai_won) {
    context.drawImage(backgroundImages[current_frame % 12], 0, 0, canvas.width, canvas.height);
    // context.font = "50px Press Start 2P";
    // context.font = "48px 'Press Start 2P' system-ui";
    drawRect(250-5, 165-5, 300+10, 120+10, '#423428');
    drawRect(250, 165, 300, 120, '#5c4832');

    context.font = "28px PressStart2P";
    context.fillStyle = "#ffffff";


    if (ai_won) {
        context.fillText("You lose!", 278, 210);
        context.fillText("AI rocks.", 285, 270);
    } else {
        context.fillText("You win!", 295, 210);
        context.fillText("AI sucks.", 285, 270);
    }

}

function gameLoop() {
    if (game_started){
        if (ai_hp <= 0) {
            render_game_over(false);
        } else if (your_hp <= 0) {
            render_game_over(true);
        } else {
            update();
            render();
        }
    } else {
        render_menu();
    }

    current_frame++;

    if (current_frame >= 10000) {
        current_frame = 0;
    }
}

setInterval(gameLoop, 1000 / FPS);

document.addEventListener('keydown', function(event) {
    switch (event.keyCode) {
        case 38: upArrow = true; break;
        case 40: downArrow = true; break;
    }
});

document.addEventListener('keyup', function(event) {
    switch (event.keyCode) {
        case 38: upArrow = false; break;
        case 40: downArrow = false; break;
    }
});
