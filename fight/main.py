import uuid

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fight.battle import (
    _ai_turn,
    _init_chat,
    _load_pokemon,
    _save_pokemon,
    _user_turn,
    get_pokemon,
)
from fight.image_caption import get_description_and_img

FIREWORK_BASE_URL = "https://api.fireworks.ai/inference/v1"
FIREWORK_API_KEY = '<FIREWORK-API-KEY>'
MODEL = "accounts/fireworks/models/llama-v3p1-70b-instruct"

AI_POKEMON_PATH = "ai_pokemon.json"
USER_POKEMON_PATH = "user_pokemon.json"


app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



###############################################################################
# Fast API Functions
###############################################################################


@app.post("/get_ai_pokemon")
async def get_ai_pokemon(input: dict):
    image_path = input["img_path"]
    image_id = str(uuid.uuid4())

    # Caption Image, Create new image
    caption_path, pokemon_image_path = get_description_and_img(image_id, image_path)

    # load image caption
    with open(caption_path, "r") as f:
        pokemon_description = f.read()

    client = _init_chat(FIREWORK_BASE_URL, FIREWORK_API_KEY)
    ai_pokemon = get_pokemon(pokemon_description, MODEL, client)
    _save_pokemon(AI_POKEMON_PATH, ai_pokemon)
    return ai_pokemon, pokemon_image_path, caption_path



@app.post("/get_user_pokemon")
async def get_user_pokemon(input: dict):
    image_path = input["img_path"]
    image_id = str(uuid.uuid4())

    # Caption Image, Create new image
    caption_path, pokemon_image_path = get_description_and_img(image_id, image_path)

    # load image caption
    with open(caption_path, "r") as f:
        pokemon_description = f.read()

    client = _init_chat(FIREWORK_BASE_URL, FIREWORK_API_KEY)
    user_pokemon = get_pokemon(pokemon_description, MODEL, client)
    _save_pokemon(USER_POKEMON_PATH, user_pokemon)
    return user_pokemon, pokemon_image_path, caption_path


@app.post("/ai_turn")
def ai_turn(input: dict):
    ai_pokemon = _load_pokemon(AI_POKEMON_PATH)
    user_pokemon = _load_pokemon(USER_POKEMON_PATH)
    client = _init_chat(FIREWORK_BASE_URL, FIREWORK_API_KEY)

    attack, insult, _ = _ai_turn(ai_pokemon, MODEL, client)
    return attack, insult


@app.post("/user_turn")
def user_turn(input: dict) -> str:
    user_attack = input["user_attack"]
    ai_pokemon = _load_pokemon(AI_POKEMON_PATH)
    user_pokemon = _load_pokemon(USER_POKEMON_PATH)
    client = _init_chat(FIREWORK_BASE_URL, FIREWORK_API_KEY)

    insult, _ = _user_turn(user_attack, user_pokemon, ai_pokemon, MODEL, client)
    return insult
