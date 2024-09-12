import base64
from io import BytesIO

import openai
import requests
from PIL import Image, ImageDraw, ImageOps

# OpenAI API Key
API_KEY = '<OPENAI-API-KEY'

# Function to encode the image
def encode_image(image_path, size=(224, 224)):
    # Open the image
    image = Image.open(image_path)
    # Resize the image
    image = image.resize(size)
    # Convert the image to base64
    buffered = BytesIO()
    if image_path.endswith(".png"):
        image.save(buffered, format="PNG")
    else:
        image.save(buffered, format="JPEG")

    return base64.b64encode(buffered.getvalue()).decode()

def decode_image(base64_string, output_path="output.png"):
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


def get_image_caption(image_path, prompt="What’s in this image?"):
    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": prompt
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 300
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()

def get_image_generation(image_description, output_path="output.png"):
    prompt = f''' Here is a description of an image: "{image_description}".
    Generate a stylized cartoon character based on the description.
    '''

    client = openai.OpenAI(
        api_key=API_KEY,
    )
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
        style='vivid',
        response_format='b64_json',
    )
  
    decode_image(response.data[0].b64_json, output_path=output_path)

def get_description_and_img(image_name, image_path):
    prompt = '''
    Give a concise description of the image.
    '''
    output_path = f"output_{image_name}.png"
    # Get the image caption
    image_caption = get_image_caption(image_path, prompt=prompt)
    image_description = image_caption['choices'][0]['message']['content']
    image_description_path = f"image_description_{image_name}.txt"

    # save the image description
    with open(image_description_path, "w") as f:
        f.write(image_description)

    get_image_generation(image_description, output_path=output_path)
    roundify_image(output_path, output_path=output_path)

    return image_description_path, output_path