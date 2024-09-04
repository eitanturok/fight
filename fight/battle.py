
import json
from typing import Any, Dict, Literal, Optional

from llama_index.llms.openai.utils import to_openai_tool
from openai import OpenAI, types
from pydantic import BaseModel

###############################################################################
# Helper Functions
###############################################################################


def _init_chat(base_url: str, api_key: str) -> OpenAI:
    client = OpenAI(base_url=base_url, api_key=api_key)
    return client


def _grow_chat(msg: str = None, tool_calls =None, tool_response: str = None, role: str = "user", messages: Optional[list[Dict[str, str]]] = None) -> list[Dict[str, str]]:
    if messages is None:
        messages = []

    def _dump_tool_calls(tool_calls):
        return [tool_call.model_dump() for tool_call in tool_calls]

    if tool_calls is not None:
        messages.append({"role": "assistant", "content": "", "tool_calls": _dump_tool_calls(tool_calls)})
    elif tool_response is not None:
        messages.append({"role": "tool", "content": json.dumps(tool_response)})
    else:
        messages.append({"role": role, "content": msg})

    return messages


def _chat(messages: list[Dict[str, str]], model:str, client: OpenAI, tools=None, temperature: float = 0.1, max_tokens=None) -> str:

    print("Chatting...")
    if tools:
        chat_completion = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            temperature=temperature,
            tool_choice="required",
            max_tokens=max_tokens,
        )
        message = chat_completion.choices[0].message
        if message.tool_calls:
            return message.tool_calls
        return message

    else:
        chat_completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        message = chat_completion.choices[0].message
        return message


def _use_the_tool(tool_call: types.chat.chat_completion_message_tool_call.Function, name_to_tool: Dict[str, callable]) -> Any:
    name = tool_call.name
    args = json.loads(tool_call.arguments)
    fn = name_to_tool[name]
    tool_response = fn(**args)
    return tool_response


def _save_pokemon(path, pokemon):
    with open(path, "w") as f:
        f.write(json.dumps(pokemon.model_dump()))

def _load_pokemon(path):
    with open(path, "r") as f:
        content = f.read()
        pokemon = Pokemon(**json.loads(content))
    return pokemon


###############################################################################
# Types
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


###############################################################################
# Get Pokemon
###############################################################################


def get_pokemon(pokemon_description: str, model: str, client: OpenAI) -> Pokemon:

    # Initialize messages
    sp = "You are a helpful assistant with access to functions. You should always use the functions provided. If the user does not specify every parameter, you can be creative. Please make all the parameter incredibly creative and funny. Use your imagination. Do not be overly verbose."
    up = f"Please create a pokemon based on the following description: {pokemon_description}. Make the pokemon funny and have a raunchy, provocative, sarcastic kind of humor. Make the hp larger than all of the attacks."
    messages = [{"role": "system", "content": sp}, {"role": "user", "content": up}]

    # Initialize tools
    name_to_tool = {"Pokemon": Pokemon}
    tools = [to_openai_tool(Pokemon)]

    # Get tool call and tool response
    tool_calls = _chat(messages, model, client, tools, max_tokens=100_000)
    tool_call = tool_calls[0].function
    tool_response = _use_the_tool(tool_call, name_to_tool)
    pokemon = tool_response
    return pokemon



###############################################################################
# AI Turn
###############################################################################


def _ai_turn(pokemon: Pokemon, model: str, client: OpenAI, messages=None) -> list[Attack, str, list[Dict[str, str]]]:
    """
    During it's turn, the AI (which is `pokemon`) attacks and insults.
    """

    # Initialize tools
    class ChooseAttack(BaseModel):
        attack: Literal[pokemon.attack1.name, pokemon.attack2.name, pokemon.attack3.name]
    name_to_attack = {pokemon.attack1.name: pokemon.attack1, pokemon.attack2.name: pokemon.attack2, pokemon.attack2.name: pokemon.attack2}
    tools = [to_openai_tool(ChooseAttack)]

    # Initialize messages
    sp = "You are a helpful assistant with access to functions. You should always use the functions provided. If the user does not specify every parameter, you can be creative. Please make all the parameter incredibly creative and funny. Use your imagination. Do not be overly verbose."
    up = "Please choose an attack."
    messages = _grow_chat(msg=sp, role="system")
    messages = _grow_chat(msg=up, role="user", messages=messages)

    # Get attack
    tool_calls = _chat(messages, model, client, tools)
    tool_call = tool_calls[0].function
    name = json.loads(tool_call.arguments)["attack"]
    attack = name_to_attack[name]

    messages = _grow_chat(tool_calls=tool_calls, messages=messages)
    messages = _grow_chat(tool_response=attack.model_dump(), messages=messages)

    # Justify attack
    up = "Please explain why you used this attack in a funny way. Talk in first person to your enemy who you are attacking. Be sarcastic. Only write 1 sentence. Be terse."
    messages = _grow_chat(up, role="user", messages=messages)

    msg = _chat(messages, model, client, max_tokens=200)
    insult = msg.content
    messages = _grow_chat(insult, role="assistant", messages=messages)

    return attack, insult, messages


###############################################################################
# User Turn
###############################################################################


def _user_turn(user_attack_name: str, user_pokemon: Pokemon, ai_pokemon: Pokemon, model: str, client: OpenAI, messages=None) -> list[str, list[Dict[str, str]]]:

    # Initialize attacks
    name_to_attack = {user_pokemon.attack1.name: user_pokemon.attack1, user_pokemon.attack2.name: user_pokemon.attack2, user_pokemon.attack2.name: user_pokemon.attack2}
    user_attack = name_to_attack[user_attack_name]

    # Initialize messages
    sp = f"You are a funny, witty, sarcastic AI model. You don't want to be overly sexual but can make raunchy jokes. You are in a pokemon style battle with a human. He is your enemy. This is your pokemon:\n{ai_pokemon.model_dump()}\nThis is your enemy human's pokemon:\n{user_pokemon.model_dump()}"
    up = f"The user just attacked you with {user_attack}. Come up with a comeback that shows you are confident and powerful. Insult the user. Be funny, and witty in your response. Talk in first person to your enemy who you are attacking. Only write 1 sentence."

    messages = _grow_chat(sp, role="system", messages=None)
    messages = _grow_chat(up, role="user", messages=messages)

    # Model insults human as a comeback
    msg = _chat(messages, model, client, max_tokens=200)
    insult = msg.content
    messages = _grow_chat(insult, role="assistant", messages=messages)

    return insult, messages
