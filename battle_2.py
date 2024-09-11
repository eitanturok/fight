# openai

import json
import os

from pydantic import BaseModel
from openai import OpenAI
from icecream import ic

API_KEY = os.environ["OPENAI_API_KEY"]
BASE_URL = 'https://api.openai.com/v1'
MODEL = 'gpt-4o-mini'


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
    client = OpenAI(base_url=base_url, api_key=api_key)
    return client


def _chat(client, model, messages, response_format=None, max_tokens=500, temperature=1):
    
    if response_format:
        completion = client.beta.chat.completions.parse(
            model=model,
            messages=messages,
            response_format=Pokemon,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        message = completion.choices[0].message.content
    else:
        chat_completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        message = chat_completion.choices[0].message
    return message
  
def get_pokemon(client, model, pokemon_description):
    
    # messages
    sp = "You are a helpful assistant that always responds with valid JSON. Do not return anything else. In the JSON schema, your response should be funny, shocking, and even outrageous. You have a raunchy, provocative, sarcastic kind of humor. If there is room to be creative, use your imagination and be contrarian, out of the box, and have hot takes. You love hot takes. When you are incredibly creative and funny, you always respond concisely, never verbosely."
    up = f"Please create a pokemon based on the following description: {pokemon_description}. Make a pokemon character with descriptions that are funny, raunchy, and sarcastic. Every attack should be very specific and should have the length of one short sentence. Attacks should be creative, contrarian, and out of the box. Please return your answer as a json schema and be concise."
    messages = [{"role": "system", "content": sp}, {"role": "user", "content": up}]
    
    pokemon_str = _chat(client, model, messages, response_format=Pokemon)
    pokemon =  json.loads(pokemon_str)
    
    return pokemon


def get_new_attacks(client, model, pokemon_description, messages):
    
    # messages
    sp = "You are a helpful assistant that always responds with valid JSON. Do not return anything else. In the JSON schema, your response should be funny, shocking, and even outrageous. You have a raunchy, provocative, sarcastic kind of humor. If there is room to be creative, use your imagination and be contrarian, out of the box, and have hot takes. You love hot takes. When you are incredibly creative and funny, you always respond concisely, never verbosely."
    up = f"Please create three attacks for this pokemon  pokemon based on the following description: {pokemon_description}. Make a pokemon character with descriptions that are funny, raunchy, and sarcastic. Every attack should be very specific and should have the length of one short sentence. Attacks should be creative, contrarian, and out of the box. Please return your answer as a json schema and be concise."
    messages = [{"role": "system", "content": sp}, {"role": "user", "content": up}]
    
    pokemon_str = _chat(client, model, messages, response_format=Pokemon)
    pokemon =  json.loads(pokemon_str)


def get_user_comeback():
    pass

if __name__ == '__main__':
    client = _init_client(base_url=BASE_URL, api_key=API_KEY)
    
    pokemon_description = "A sassy, young man with a bad attitude and a penchant for eye-rolling."
    pokemon = get_pokemon(client, MODEL, pokemon_description)
    ic(pokemon)