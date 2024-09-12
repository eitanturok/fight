from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.battle3 import get_pokemon, select_attack, get_insult, get_comeback, _load_pokemon


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
    img_path = input["img_path"]
    return get_pokemon(img_path, AI_POKEMON_PATH)


@app.post("/get_user_pokemon")
async def get_user_pokemon(input: dict):
    img_path = input["img_path"] 
    return get_pokemon(img_path, USER_POKEMON_PATH)


@app.post("/ai_turn")
def ai_turn(input: dict):
    ai_pokemon = _load_pokemon(AI_POKEMON_PATH)
    attack = select_attack(ai_pokemon)
    insult = get_insult(attack)
    return attack, insult


@app.post("/user_turn")
def user_turn(input: dict) -> str:
    ai_pokemon = _load_pokemon(AI_POKEMON_PATH)
    user_pokemon = _load_pokemon(USER_POKEMON_PATH)
    user_attack_name = input["user_attack"]
    
    comeback = get_comeback(user_pokemon, ai_pokemon, user_attack_name)
    return comeback
