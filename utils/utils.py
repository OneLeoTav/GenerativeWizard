import diffusers
from diffusers import AutoPipelineForText2Image

import torch

import base64
import PIL
import io

from typing import Union, Optional, Tuple


def load_img_pipeline(device: Union[str, torch.device]) -> AutoPipelineForText2Image:
    """
    Load the text-to-image generation model pipeline.

    Args:
        device (Union[str, torch.device]): The device on which to load the model,
            either a string specifying a device (e.g., 'cuda:0') or a torch.device object.

    Returns:
        AutoPipelineForText2Image: The loaded text-to-image generation model pipeline.

    Notes:
        If the device is 'cuda:0' or 'cuda', the model will be loaded with dtype=torch.float16
        and variant="fp16" for performance optimization. Otherwise, the model will be loaded
        with dtype=torch.float32 and variant="fp32".
    """

    if device in ['cuda:0', 'cuda']:
        return AutoPipelineForText2Image.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float16,
            variant="fp16",
        ).to(device)
    else:
        return AutoPipelineForText2Image.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            low_cpu_mem_usage=True,
            variant="fp16",
        ).to(device)

def generate_image(prompt: str, img_pipeline: AutoPipelineForText2Image) -> PIL.Image.Image:
    """
    Generate an image based on the provided text prompt.

    Args:
        prompt (str): The text prompt for image generation.
        img_pipeline (AutoPipelineForText2Image): The text-to-image generation model pipeline.

    Returns:
        PIL.Image.Image: The generated image as a PIL.Image.Image.
    """
    image = img_pipeline(prompt).images[0]
    return image


def pil_image_to_base64(
    pil_image: PIL.Image.Image,
    dimensions: Optional[Tuple[int, int]] = None
) -> str:
    """
    Convert a PIL Image to a base64-encoded string.

    Args:
        pil_image (PIL.Image.Image): The PIL Image object to be converted.
        dimensions (Optional[Tuple[int, int]]): Optional dimensions (width, height) for the image.

    Returns:
        str: The base64-encoded representation of the input PIL Image.
    """
    buffered = io.BytesIO()

    if dimensions:  # Resize the image if necessary
        pil_image = pil_image.resize(dimensions)

    pil_image.save(buffered, format="PNG")
    base64_encoded_image = base64.b64encode(buffered.getvalue()).decode()

    # Another option could have been:
    # with io.BytesIO() as f:
    #     pil_image.save(f, format="PNG")
    #     contents = f.getvalue()
    # base64_encoded_image = base64.b64encode(contents).decode()
    return base64_encoded_image
