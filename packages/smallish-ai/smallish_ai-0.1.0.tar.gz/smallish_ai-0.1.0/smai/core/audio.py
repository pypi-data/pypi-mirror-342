from typing import Optional, Literal
from pathlib import Path
import time
from litellm import transcription, speech
from .config import CONFIG

def is_audio_file(file_path: str) -> bool:
    """Check if the given file is an audio file based on its extension.
    
    Args:
        file_path: Path to the file to check
        
    Returns:
        bool: True if the file has a recognized audio extension, False otherwise
    """
    audio_extensions = {'.mp3', '.mp4', '.mpeg', '.mpga', '.m4a', '.wav', '.webm'}
    return Path(file_path).suffix.lower() in audio_extensions

def transcribe_audio(model: str, file_path: str, prompt: Optional[str] = None) -> str:
    """Transcribe audio file using the specified model.
    
    Args:
        model: The model to use for transcription
        file_path: Path to the audio file to transcribe
        prompt: Optional prompt to guide the transcription
        
    Returns:
        str: The transcribed text from the audio file
    """
    with open(file_path, "rb") as audio_file:
        response = transcription(
            model=model,
            file=audio_file,
            prompt=prompt
        )
    return response["text"]

def generate_speech(model: str, text: str, voice: str = "alloy", output_file: Optional[str] = None) -> str:
    """Generate speech from text using the specified model and voice.
    
    Args:
        model: The model to use for speech generation
        text: The text to convert to speech
        voice: The voice to use (default: "alloy")
        output_file: Optional path for the output file. If None, a timestamped file
                     will be created in the configured directory
        
    Returns:
        str: Path to the generated audio file
    """
    if output_file is None:
        # Use configured directory
        audio_dir = Path(CONFIG["generated_audio_dir"])
        audio_dir.mkdir(parents=True, exist_ok=True)
        timestamp = int(time.time())
        output_file = audio_dir / f"output_{timestamp}.mp3"
    
    speech_file_path = Path(output_file)
    response = speech(
        model=model,
        voice=voice,
        input=text
    )
    response.stream_to_file(speech_file_path)
    return str(speech_file_path)

def process_audio_input(file_path: str, model: str, prompt: Optional[str] = None) -> dict:
    """Process audio input and return a message dictionary.
    
    Args:
        file_path: Path to the audio file to process
        model: The model to use for transcription
        prompt: Optional prompt to guide the transcription
        
    Returns:
        dict: A message dictionary containing the transcribed text and metadata
    """
    transcription = transcribe_audio(model, file_path, prompt)
    return {
        "type": "audio_input",
        "text": transcription,
        "original_file": file_path
    }

def process_audio_output(model: str, text: str, voice: str = "alloy", output_file: Optional[str] = None) -> str:
    """Process audio output and return the path to the generated audio file.
    
    Args:
        model: The model to use for speech generation
        text: The text to convert to speech
        voice: The voice to use (default: "alloy")
        output_file: Optional path for the output file
        
    Returns:
        str: Path to the generated audio file
    """
    return generate_speech(model, text, voice, output_file)
