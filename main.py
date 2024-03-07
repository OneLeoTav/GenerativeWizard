from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from pathlib import Path

import base64
from PIL import Image
from io import BytesIO
import time
import torch

from utils.utils import (
    load_img_pipeline,
    generate_image,
    pil_image_to_base64,
)

# Load the model outside the route handler and any other function to avoid loading it back and forth
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
text_to_image_pipeline = load_img_pipeline(device)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/prompt")
def render_generated_image(generate_input: str = Form(...)):
    """
    Render a generated image based on the provided text input.

    Args:
        generate_input (str): The text input for generating the image.

    Returns:
        dict: A dictionary containing the base64-encoded image and the original prompt.
    """
    prompt = str(generate_input)

    if prompt:  # Check if prompt is not empty or None
        generated_image = generate_image(prompt, text_to_image_pipeline)
        width, height = 400, 400  # Set width and height (for a better display)
        resized_image = generated_image.resize((width, height))
        base64_encoded_image = pil_image_to_base64(resized_image)
        return {
            'base64_image': base64_encoded_image,
            'original_prompt': prompt,
        }