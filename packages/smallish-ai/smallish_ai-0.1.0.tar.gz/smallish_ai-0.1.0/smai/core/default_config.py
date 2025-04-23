"""Default configuration for smai."""
from pathlib import Path
from appdirs import user_config_dir, user_data_dir

# Default models to use for different tasks
DEFAULT_MODELS = {
    "text": "anthropic/claude-3-5-sonnet-latest",
    "image": "dall-e-3",
    "audio": "tts"
}

# Default tools directory
TOOLS_DIR = Path(user_config_dir("smai")) / "tools"

# Default directories for generated content
GENERATED_IMAGES_DIR = Path(user_data_dir("smai")) / "generated" / "images"
GENERATED_AUDIO_DIR = Path(user_data_dir("smai")) / "generated" / "audio"
