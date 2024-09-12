# firework + instructor
import json
import os
import uuid
from random import randrange
from typing import Dict, Union, Optional

import instructor
from pydantic import BaseModel
from openai import OpenAI
from icecream import ic

from image_caption import get_description_and_img


API_KEY = os.environ["FIREWORKS_API_KEY"] # fw_3ZJszLDVoKbcjnAfFTopn7Gw
BASE_URL = "https://api.fireworks.ai/inference/v1"
MODEL = "accounts/fireworks/models/llama-v3p1-70b-instruct"


###############################################################################
# Helper Functions
###############################################################################


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
    
    
def _init_client(base_url: Optional[str] = None, api_key: Optional[str] = None) -> OpenAI:
    if api_key is None:
        api_key = os.environ["FIREWORKS_API_KEY"] # fw_3ZJszLDVoKbcjnAfFTopn7Gw
    if base_url is None:
        base_url = "https://api.fireworks.ai/inference/v1"

    _client = OpenAI(base_url=base_url, api_key=api_key)
    client = instructor.from_openai(_client)
    return client


def _chat(
    messages: list[Dict[str, str]],
    client: Optional[OpenAI] = None,
    model:str = 'accounts/fireworks/models/llama-v3p1-70b-instruct',
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    response_model=None,
    temperature: float = 0.1,
    max_tokens=None,
    ) -> Union[str, BaseModel]:
    
    if client is None:
        client = _init_client(base_url=base_url, api_key=api_key)
    
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        response_model=response_model,
    )
    return completion.choices[0].message.content if response_model is None else completion
        
        
def _save_pokemon(path: str, pokemon: Pokemon):
    with open(path, "w") as f:
        f.write(json.dumps(pokemon.model_dump()))

def _load_pokemon(path: str):
    with open(path, "r") as f:
        content = f.read()
        pokemon = Pokemon(**json.loads(content))
    return pokemon


###############################################################################
# Get Pokemon
###############################################################################


def generate_pokemon(pokemon_description: str) -> Pokemon:
    
    # messages
    sp = "You are a helpful assistant with access to functions. You should always use the functions provided. If the user does not specify every parameter, you can be creative. Please make all the parameter incredibly creative and funny. Use your imagination. Do not be overly verbose."
    up = f"Please create a pokemon based on the following description: {pokemon_description}. Make the pokemon funny and have a raunchy, provocative, sarcastic kind of humor. Make the hp larger than all of the attacks."
    messages = [{"role": "system", "content": sp}, {"role": "user", "content": up}]
        
    # make pokemon
    pokemon = _chat(messages, response_model=Pokemon)
    
    return pokemon

    
def get_pokemon(image_path: str, pokemon_path: str) -> tuple[Pokemon, str, str]:
    image_id = str(uuid.uuid4())

    # Caption image, create new image
    pokemon_description_path, pokemon_image_path = get_description_and_img(image_id, image_path)

    # load image caption
    with open(pokemon_description_path, "r") as f:
        pokemon_description = f.read()

    pokemon = generate_pokemon(pokemon_description)
    _save_pokemon(pokemon_path,pokemon)
    return pokemon, pokemon_image_path, pokemon_description_path


###############################################################################
# AI Turn
###############################################################################


def get_insult(attack: Attack) -> str:

    # Initialize messages
    sp = "You are an incredibly creative and funny AI who uses your imagination and loves to be contrarian and out-of-the-box."
    up = f"You just used the attack: {attack.model_dump()}.\nPlease explain why you used this attack in a funny way. Talk in first person to your enemy who you are attacking. Feel free to insult them. Be sarcastic. Only write 1 sentence. Be terse."
    messages = [{"role": "system", "content": sp}, {"role": "user", "content": up}]
    
    # Generate insult
    insult: str = _chat(messages)
    return insult
    
    
def select_attack(pokemon: Pokemon) -> Attack:
    # Randomly select an attack
    idx_to_attack = {0: pokemon.attack1, 1: pokemon.attack2, 2: pokemon.attack3}
    attack_idx = randrange(3)
    attack = idx_to_attack[attack_idx]
    return attack
    

###############################################################################
# User Turn
###############################################################################


def get_comeback(user_pokemon: Pokemon, ai_pokemon: Pokemon, user_attack_name: str) -> str:
    
    # Initialize user attack
    name_to_attack = {user_pokemon.attack1.name: user_pokemon.attack1, user_pokemon.attack2.name: user_pokemon.attack2, user_pokemon.attack2.name: user_pokemon.attack2}
    user_attack = name_to_attack[user_attack_name]
    
    # Initialize messages
    sp = f"You are a funny, witty, sarcastic AI model. You don't want to be overly sexual but can make raunchy jokes. You are in a pokemon style battle with a human. He is your enemy. This is your pokemon:\n{ai_pokemon.model_dump()}\nThis is your enemy human's pokemon:\n{user_pokemon.model_dump()}"
    up = f"The user just attacked you with {user_attack}. Come up with a comeback that shows you are confident and powerful. Insult the user. Be funny, and witty in your response. Talk in first person to your enemy who you are attacking. Only write 1 sentence."
    messages = [{"role": "system", "content": sp}, {"role": "user", "content": up}]
      
    # Get comeback
    comeback: str = _chat(messages)
    
    return comeback

if __name__ == '__main__':

    pokemon_description = "A sassy, young man with a bad attitude and a penchant for eye-rolling."    
    user_pokemon = generate_pokemon(pokemon_description)
    ic(user_pokemon)
    
    pokemon_description = "A fat train driving recklessly that is fat."    
    ai_pokemon = generate_pokemon(pokemon_description)
    ic(ai_pokemon)
    
    user_attack_name = user_pokemon.attack1.name
    ic(user_pokemon.attack1)
    
    # comeback = _get_comeback(client, model, user_pokemon, ai_pokemon, user_attack_name)
    # ic(comeback)
    
    # attack, insult = ai_turn(ai_pokemon, model, client)
    # ic(attack)
    # ic(insult)