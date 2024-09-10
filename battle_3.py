# firework + instructor
import os
from typing import Dict, Union

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


def _chat(messages: list[Dict[str, str]], model:str, client: OpenAI, response_model=None, temperature: float = 0.1, max_tokens=None) -> Union[str, BaseModel]:
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        response_model=response_model,
    )
    return completion.choices[0].message.content if response_model is None else completion
        

def get_pokemon(client, model, pokemon_description):
    
    # messages
    sp = "You are a helpful assistant with access to functions. You should always use the functions provided. If the user does not specify every parameter, you can be creative. Please make all the parameter incredibly creative and funny. Use your imagination. Do not be overly verbose."
    up = f"Please create a pokemon based on the following description: {pokemon_description}. Make the pokemon funny and have a raunchy, provocative, sarcastic kind of humor. Make the hp larger than all of the attacks."
    messages = [{"role": "system", "content": sp}, {"role": "user", "content": up}]
        
    # make pokemon
    pokemon = _chat(messages, model, client, response_model=Pokemon)
    
    return pokemon


def get_comeback(client: OpenAI, model: str, user_pokemon: Pokemon, ai_pokemon: Pokemon, user_attack_name: str):
    
    # Initialize user attack
    name_to_attack = {user_pokemon.attack1.name: user_pokemon.attack1, user_pokemon.attack2.name: user_pokemon.attack2, user_pokemon.attack2.name: user_pokemon.attack2}
    user_attack = name_to_attack[user_attack_name]
    
    # Initialize messages
    sp = f"You are a funny, witty, sarcastic AI model. You don't want to be overly sexual but can make raunchy jokes. You are in a pokemon style battle with a human. He is your enemy. This is your pokemon:\n{ai_pokemon.model_dump()}\nThis is your enemy human's pokemon:\n{user_pokemon.model_dump()}"
    up = f"The user just attacked you with {user_attack}. Come up with a comeback that shows you are confident and powerful. Insult the user. Be funny, and witty in your response. Talk in first person to your enemy who you are attacking. Only write 1 sentence."
    messages = [{"role": "system", "content": sp}, {"role": "user", "content": up}]
      
    # Get comeback
    comeback = _chat(messages, model, client)
    
    return comeback


if __name__ == '__main__':

    model = MODEL
    client = _init_client(base_url=BASE_URL, api_key=API_KEY)
    
    pokemon_description = "A sassy, young man with a bad attitude and a penchant for eye-rolling."    
    user_pokemon = get_pokemon(client, model, pokemon_description)
    ic(user_pokemon)
    
    pokemon_description = "A train driving recklessly."    
    ai_pokemon = get_pokemon(client, model, pokemon_description)
    ic(ai_pokemon)
    
    user_attack_name = user_pokemon.attack1.name
    ic(user_attack_name)
    
    comeback = get_comeback(client, model, user_pokemon, ai_pokemon, user_attack_name)
    ic(comeback)
    
    
