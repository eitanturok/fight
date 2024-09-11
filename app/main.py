import os
import uuid

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.battle3 import get_pokemon, select_attack, get_insult, get_comeback
from app.battle import (
    _ai_turn,
    _init_chat,
    _load_pokemon,
    _save_pokemon,
    _user_turn,
    get_pokemon,
)


API_KEY = os.environ["FIREWORKS_API_KEY"] # fw_3ZJszLDVoKbcjnAfFTopn7Gw
BASE_URL = "https://api.fireworks.ai/inference/v1"
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
    client = _init_chat(BASE_URL, API_KEY)
    return get_pokemon(input["img_path"], AI_POKEMON_PATH, MODEL, client)


@app.post("/get_user_pokemon")
async def get_user_pokemon(input: dict):
    client = _init_chat(BASE_URL, API_KEY)
    return get_pokemon(input["img_path"], USER_POKEMON_PATH, MODEL, client)

@app.post("/ai_turn")
def ai_turn(input: dict):
    ai_pokemon = _load_pokemon(AI_POKEMON_PATH)
    client = _init_chat(BASE_URL, API_KEY)

    attack = select_attack(ai_pokemon)
    insult = get_insult(MODEL, client, attack)
    return attack, insult


@app.post("/user_turn")
def user_turn(input: dict) -> str:
    user_attack_name = input["user_attack"]
    ai_pokemon = _load_pokemon(AI_POKEMON_PATH)
    user_pokemon = _load_pokemon(USER_POKEMON_PATH)
    client = _init_chat(BASE_URL, API_KEY)
    
    comeback = get_comeback(client, MODEL, user_pokemon, ai_pokemon, user_attack_name)
    return comeback
