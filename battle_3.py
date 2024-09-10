# firework + instructor
import os

import jsonref
import instructor
from pydantic import BaseModel
from openai import OpenAI
from icecream import ic


API_KEY = os.environ["FIREWORKS_API_KEY"] # fw_3ZJszLDVoKbcjnAfFTopn7Gw
BASE_URL = "https://api.fireworks.ai/inference/v1"
MODEL = "accounts/fireworks/models/llama-v3p1-70b-instruct"


class Attack(BaseModel):
    accuracy: int
    power: int
    name: str
    description: str


class Pokemon(BaseModel):
    name: str
    type: str
    hp: int
    description: str
    attack1: Attack
    attack2: Attack
    attack3: Attack
    
    
def _init_client(base_url: str, api_key: str) -> OpenAI:
    _client = OpenAI(base_url=base_url, api_key=api_key)
    client = instructor.from_openai(_client)
    return client

def get_pokemon(client, model, pokemon_description):
    
    # messages
    sp = "You are a helpful assistant with access to functions. You should always use the functions provided. If the user does not specify every parameter, you can be creative. Please make all the parameter incredibly creative and funny. Use your imagination. Do not be overly verbose."
    up = f"Please create a pokemon based on the following description: {pokemon_description}. Make the pokemon funny and have a raunchy, provocative, sarcastic kind of humor. Make the hp larger than all of the attacks."
    messages = [{"role": "system", "content": sp}, {"role": "user", "content": up}]
        
    # make pokemon
    pokemon = client.chat.completions.create(
        model=model,
        messages=messages,
        response_model=Pokemon,
    )
    pokemon_json = pokemon.model_dump()
    
    return pokemon_json



client = _init_client(base_url=BASE_URL, api_key=API_KEY)
pokemon_description = "A sassy, young man with a bad attitude and a penchant for eye-rolling."
model = MODEL
pokemon = get_pokemon(client, model, pokemon_description)
