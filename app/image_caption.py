import base64
import os
from io import BytesIO

import openai
import requests
from PIL import Image, ImageDraw, ImageOps
from icecream import ic

###############################################################################
# Helper Functions
###############################################################################


def _get_api_key():
    return os.environ["OPENAI_API_KEY"]


def _encode_image(image_path: str, size=(224, 224)):
    
    # Prepare the image
    image = Image.open(image_path)
    image = image.resize(size)
    buffered = BytesIO()
    
    # Save image
    if image_path.endswith(".png"):
        image.save(buffered, format="PNG")
    else:
        image.save(buffered, format="JPEG")

    encoded_image = base64.b64encode(buffered.getvalue()).decode()
    return encoded_image


def _decode_image(base64_string, output_path="output.png"):
  imgdata = base64.b64decode(base64_string)
  with open(output_path, 'wb') as f:
    f.write(imgdata)


def roundify_image(image_path, output_path="output_modif.png"):
    im = Image.open(image_path)
    size = im.size
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    output.save(output_path)


###############################################################################
# Main Functions
###############################################################################


def get_image_caption(image_path, prompt="What's in this image?"):

    # headers
    api_key = _get_api_key()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
        }
    
    # payload
    base64_image = _encode_image(image_path)
    
    messages = [{
        "role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
            ]
        }]
    payload = {
        "model": "gpt-4o-mini",
        "messages": messages,
        "max_tokens": 300
        }

    # hit openai endpoint
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()


def get_image_generation(image_description, output_path="output.png"):
    prompt = f''' Here is a description of an image: "{image_description}".
    Generate a stylized cartoon character based on the description.
    '''

    api_key = _get_api_key()
    client = openai.OpenAI(api_key=api_key)
    
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
        style='vivid',
        response_format='b64_json',
    )
  
    _decode_image(response.data[0].b64_json, output_path=output_path)


def get_description_and_img(image_name: str, image_path: str):
    prompt = '''Give a one sentence description of the image. Be specific and
             concise. Answer directly; do not say 'this image contains', just
             provide the description.'''
    output_path = f"output_{image_name}.png"
    
    # Get and save image caption
    image_caption = get_image_caption(image_path, prompt=prompt)
    image_description = image_caption['choices'][0]['message']['content']
    image_description_path = f"image_description_{image_name}.txt"

    with open(image_description_path, "w") as f:
        f.write(image_description)

    # Generate, round, and save generated image
    get_image_generation(image_description, output_path=output_path)
    roundify_image(output_path, output_path=output_path)

    return image_description_path, output_path