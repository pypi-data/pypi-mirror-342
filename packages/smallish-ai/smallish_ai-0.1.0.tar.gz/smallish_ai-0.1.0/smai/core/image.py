import base64
import os
import requests
import pylibmagic
import magic
import time
from pathlib import Path
from litellm import image_generation
from litellm.utils import supports_pdf_input
from .config import CONFIG

def get_filename_from_prompt(prompt_text: str, directory: Path) -> Path:
    """Generate a filename based on the prompt text.
    
    Args:
        prompt_text (str): The prompt text to use for the filename
        directory (Path): The directory where the file will be saved
        
    Returns:
        Path: A unique filename path based on the prompt
    """
    # Take first 15 chars of prompt, replace whitespace with underscores
    base_name = prompt_text[:15].strip().replace(" ", "_")
    # Remove any non-alphanumeric characters except underscores
    base_name = ''.join(c for c in base_name if c.isalnum() or c == '_')
    # Ensure we have at least some valid characters
    if not base_name:
        base_name = "image"
    
    # Check if file exists and add numeric suffix if needed
    counter = 0
    file_path = directory / f"{base_name}.png"
    while file_path.exists():
        counter += 1
        file_path = directory / f"{base_name}_{counter}.png"
    
    return file_path

def is_image_file(file_path: str) -> bool:
    """Check if a file is an image based on its MIME type.
    
    Args:
        file_path (str): Path to the file to check
        
    Returns:
        bool: True if the file is an image, False otherwise
    """
    mime = magic.Magic(mime=True)
    file_type = mime.from_file(file_path)
    return file_type.startswith('image/')

def encode_image(image_path: str) -> str:
    """Encode an image file as a base64 string.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        str: Base64-encoded string representation of the image
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def generate_image(model: str, prompt: str, output: str = None) -> str:
    """Generate an image using the specified AI model and prompt.
    
    Args:
        model (str): The image generation model to use
        prompt (str): Text description of the image to generate
        output (str, optional): Output path for the generated image
        
    Returns:
        str: Path to the generated image file
    """
    response = image_generation(prompt=prompt, model=model)

    image_url = response.data[0]['url']
    
    # Download the image
    image_data = requests.get(image_url).content
    
    if output:
        if os.path.isdir(output):
            output_dir = Path(output)
            filename = get_filename_from_prompt(prompt, output_dir)
        else:
            filename = output
    else:
        # Use configured directory
        images_dir = Path(CONFIG["generated_images_dir"])
        images_dir.mkdir(parents=True, exist_ok=True)
        filename = get_filename_from_prompt(prompt, images_dir)
    
    with open(filename, "wb") as file:
        file.write(image_data)
    
    return str(filename)

def is_pdf_file(file_path: str) -> bool:
    """Check if a file is a PDF based on its MIME type.
    
    Args:
        file_path (str): Path to the file to check
        
    Returns:
        bool: True if the file is a PDF, False otherwise
    """
    mime = magic.Magic(mime=True)
    file_type = mime.from_file(file_path)
    return file_type == 'application/pdf'

def get_pdf_message(file_path: str, model: str = None):
    """Get message format for PDF files.
    
    Args:
        file_path (str): Path to the PDF file
        model (str, optional): The model to use for processing the PDF
        
    Returns:
        dict: Message object in the format expected by the API
        
    Raises:
        ValueError: If the model doesn't support PDF input
    """
    if not model or not supports_pdf_input(model):
        raise ValueError(f"Model {model} does not support PDF input")
    with open(file_path, "rb") as pdf_file:
        encoded_file = base64.b64encode(pdf_file.read()).decode("utf-8")
        return {
            "type": "image_url",
            "image_url": {
                "url": f"data:application/pdf;base64,{encoded_file}"
            }
        }

def get_image_message(file_path: str):
    """Get message format for image files.
    
    Args:
        file_path (str): Path to the image file
        
    Returns:
        dict: Message object in the format expected by the API
    """
    base64_image = encode_image(file_path)
    return {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
        }
    }

