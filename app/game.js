const FPS = 6;
const OFFLINE = true;

let humanState = {
    hp: 100,
    attacks: [
        {
            title: "Base human attack 1",
            power: 10,
            accuracy: 0.9
        },
        {
            title: "Base human attack 2",
            power: 20,
            accuracy: 0.7
        },
        {
            title: "Base human attack 3",
            power: 30,
            accuracy: 0.5
        }
    ],
    homeLoc: [185, 250],
    currLoc: [100, 200],
    image: new Image(),
    hitFrame: -1000,
    missFrame: -1000,
    hitMovement: [
        [212, 212],
        [249, 176],
        [298, 143],
        [362, 139],
        [422, 157],
        [420, 165],
        [373, 183],
        [328, 201],
        [285, 220],
        [234, 233]
    ],
    missMovement: [
        [212, 212, 0],
        [249, 176, 0],
        [298, 143, 0],
        [362, 139, 0],
        [422, 157, 60],
        [420, 165, 120],
        [373, 183, 180],
        [328, 201, 240],
        [285, 220, 300],
        [234, 233, 0]
    ],
    homeOffset: false
}
humanState.image.src = '../assets/human.png';

let aiState = {
    hp: 100,
    attacks: [
        {
            title: "Punch stomach",
            power: 10,
            accuracy: 0.9
        },
        {
            title: "Punch chest",
            power: 20,
            accuracy: 0.7
        },
        {
            title: "Punch face",
            power: 30,
            accuracy: 0.5
        }
    ],
    homeLoc: [518, 170],
    currLoc: [110, 110],
    image: new Image(),
    hitFrame: -1000,
    missFrame: -1000,
    hitMovement: [
        [490, 160],
        [439, 152],
        [378, 169],
        [329, 208],
        [294, 250],
        [295, 262],
        [343, 245],
        [390, 224],
        [435, 201],
        [484, 179]
    ],
    missMovement: [
        [490, 160, 0],
        [439, 152, 0],
        [378, 169, 0],
        [329, 208, 0],
        [294, 250, 300],
        [295, 262, 240],
        [343, 245, 180],
        [390, 224, 120],
        [435, 201, 60],
        [484, 179, 0]
    ],
    homeOffset: true
}
aiState.image.src = '../assets/ai.png';

let game_started = false;
let currentFrame = 0;

let backgroundImages = [];
for (let i = 0; i < 12; i++) {
    let img = new Image();
    img.src = '../assets/battle_backgrounds/frame_' + i + '.png';
    backgroundImages.push(img);
}

let explosionImages = [];
for (let i = 0; i < 6; i++) {
    let img = new Image();
    img.src = '../assets/explosions/frame_' + i + '.png';
    explosionImages.push(img);
}

let canvas = document.getElementById('game');
let context = canvas.getContext('2d');

// updating player
function updatePlayerProfile(result, name, playerState) {
    document.getElementById(name + "-card").style.display = "flex";

    if (!OFFLINE) {
        document.getElementById(name + "-name").innerText = result[0]["name"];
        document.getElementById(name + "-description").innerText = result[0]["description"];
        document.getElementById(name + "-hp").innerText = "HP: " + result[0]["hp"];
        document.getElementById(name + "-attacks").innerText = "Attacks: " + result[0]["attack1"]["name"] + ", " + result[0]["attack2"]["name"] + ", " + result[0]["attack3"]["name"];
        
        playerState.image.src = result[1];
        
        for (let i = 0; i < 3; i++) {
            playerState.attacks[i] = {
                title: result[0]["attack" + (i+1)]["name"],
                power: result[0]["attack" + (i+1)]["power"],
                accuracy: result[0]["attack" + (i+1)]["accuracy"],
                description: result[0]["attack" + (i+1)]["description"]
            }
        }
    }
}

function updatePlayerProfileCalls(file, name, playerState) {
    fetch("http://localhost:8000/get_" + name + "_pokemon", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({img_path: file["name"]}),
    }).then(result => {
        updatePlayerProfile(result.json(), name, playerState);
    });

    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById(name + "_image_show").src = e.target.result;
        }
        reader.readAsDataURL(file);
    }
}

document.getElementById('human-image').addEventListener('change', function(event) {
    updatePlayerProfile(event.target.files[0], "human", humanState);
});

document.getElementById('ai-image').addEventListener('change', function(event) {
    updatePlayerProfile(event.target.files[0], "ai", aiState);
});

function animationsOver(offset) {
    let frame = currentFrame - offset

    if (humanState.hitFrame + 9 >= frame || humanState.missFrame + 9 >= frame) {
        return false;
    }
    if (aiState.hitFrame + 9 >= frame || aiState.missFrame + 9 >= frame) {
        return false;
    }
    return true;
}

function useAttack(attackNumber) {
    if (!animationsOver(0) || aiState.hp <= 0 || humanState.hp <= 0) {
        return;
    }

    let power = humanState.attacks[attackNumber]["power"];
    let accuracy = humanState.attacks[attackNumber]["accuracy"];

    if (Math.random() < accuracy) {
        aiState.hp -= power;
        attack_hit = true;

        humanState.hitFrame = currentFrame;
    } else {
        humanState.missFrame = currentFrame;
    }

    document.getElementById("trash-talk").innerText = "You chose " + humanState.attacks[attackNumber]["title"] + " attack! " + humanState.attacks[attackNumber]["description"];

    // TODO: Call AI attack with attack_hit
    // _human_turn({human_attack: attacks[attack_number]["title"]}).then(result => {
    //     console.log(result);
    //     document.getElementById("trash-talk").innerText = result;
    // });
    // const response_json = await _human_turn({human_attack: attacks[attack_number]["title"]});
    // document.getElementById("trash_talk").innerText = response_json;
}

async function _human_turn(data) {
    const response = await fetch('http://localhost:8000/human_turn', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });

    return await response.json();
}

function startGame(){
    game_started = true;

    document.getElementById('start-button').style.display = "none";

    gameDescription = `<div class="card" style="width: 810px;">
            <div class="card-body" id="trash-talk">
                This is some text within a card body. This is some text within a card body.
            </div>
        </div>
        <div class="row" style="margin: 0 auto; width: 800px;">`

    for (let i = 0; i < 3; i++) {
        gameDescription = gameDescription + `<div class="col">
                <div class="card" style="width: 100%;">
                    <div class="card-body">
                        <h5 class="card-title">${humanState.attacks[i]["title"]}</h5>
                        <p class="card-text">
                            Power: ${humanState.attacks[i]["power"]}
                            Acc: ${humanState.attacks[i]["accuracy"]}
                        </p>
                        <button onclick="useAttack(${i})" class="btn btn-danger">Use</button>
                    </div>
                </div>
            </div>`;
    }
    gameDescription = gameDescription + "</div>"

    document.getElementById('game_description').innerHTML = gameDescription
}

function drawRect(x, y, w, h, color) {
    context.fillStyle = color;
    context.fillRect(x, y, w, h);
}

function drawRotatedImage(image, x, y, width, height, angle) { 
    context.save();
    context.translate(x, y);
    context.rotate(angle * (Math.PI/180));
    context.drawImage(image, 0, 0, width, height);
    context.restore();
}

function renderMenu() {
    context.drawImage(backgroundImages[currentFrame % 12], 0, 0, canvas.width, canvas.height);

    drawRect(150-5, 165-5, 500+10, 120+10, '#423428');
    drawRect(150, 165, 500, 120, '#5c4832');

    context.font = "28px PressStart2P";
    context.fillStyle = "#ffffff";
    context.fillText("Select Characters", 166, 210);
    context.fillText("and Press Start!", 182, 270);
}

function animatePlayer(state, otherState) {
    if (state.hitFrame + 9 >= currentFrame) {
        context.drawImage(state.image, state.hitMovement[currentFrame - state.hitFrame][0], state.hitMovement[currentFrame - state.hitFrame][1], 110, 110);
        // for 6 frames
        if (state.hitFrame + 4 < currentFrame) {
            context.drawImage(explosionImages[currentFrame - state.hitFrame - 4], otherState.homeLoc[0] - 10, otherState.homeLoc[1] - 10, 130, 130);
        }
    } else if (state.missFrame + 9 >= currentFrame) {
        drawRotatedImage(state.image, state.missMovement[currentFrame - state.missFrame][0], state.missMovement[currentFrame - state.missFrame][1], 110, 110, state.missMovement[currentFrame - state.missFrame][2]);
    } else {
        let offset = state.homeOffset;
        context.drawImage(state.image, state.homeLoc[0] + (6 * ((Math.floor((currentFrame + 2*offset) / 4) + 1) % 2)), state.homeLoc[1], 110, 110);
    }
}

function renderGame() {
    context.drawImage(backgroundImages[currentFrame % 12], 0, 0, canvas.width, canvas.height);

    animatePlayer(humanState, aiState);
    animatePlayer(aiState, humanState);

    context.font = "12x PressStart2P";
    context.fillStyle = "#ffffff";
    context.fillText("Human HP: " + humanState.hp, 50, 430);
    context.fillText("AI HP: " + aiState.hp, 510, 50);
}

function renderGameOver(ai_won) {
    context.drawImage(backgroundImages[currentFrame % 12], 0, 0, canvas.width, canvas.height);

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
        if (aiState.hp <= 0 && animationsOver(5)) {
            renderGameOver(false);
        } else if (humanState.hp <= 0 && animationsOver(5)) {
            renderGameOver(true);
        } else {
            renderGame();
        }
    } else {
        renderMenu();
    }

    currentFrame++;
    currentFrame = currentFrame % 10000;
}

setInterval(gameLoop, 1000 / FPS);