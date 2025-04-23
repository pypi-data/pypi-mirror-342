"""Configuration management for smai."""
import os
import sys
import shutil
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec
from appdirs import user_config_dir

# Import default configuration
from .default_config import (
    DEFAULT_MODELS, 
    TOOLS_DIR as DEFAULT_TOOLS_DIR,
    GENERATED_IMAGES_DIR as DEFAULT_IMAGES_DIR,
    GENERATED_AUDIO_DIR as DEFAULT_AUDIO_DIR
)

def get_config_path() -> Path:
    """Get the platform-specific config file path."""
    config_dir = Path(user_config_dir("smai"))
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.py"

def load_user_config():
    """Load user configuration, falling back to defaults if not found."""
    config_path = get_config_path()
    
    if not config_path.exists():
        return {
            "default_models": DEFAULT_MODELS, 
            "tools_dir": DEFAULT_TOOLS_DIR,
            "generated_images_dir": DEFAULT_IMAGES_DIR,
            "generated_audio_dir": DEFAULT_AUDIO_DIR
        }
    
    try:
        # Load the user's config.py as a module
        spec = spec_from_file_location("user_config", config_path)
        user_config = module_from_spec(spec)
        spec.loader.exec_module(user_config)
        
        # Merge with defaults, preferring user settings
        config = {
            "default_models": DEFAULT_MODELS.copy(),
            "tools_dir": DEFAULT_TOOLS_DIR,
            "generated_images_dir": DEFAULT_IMAGES_DIR,
            "generated_audio_dir": DEFAULT_AUDIO_DIR
        }
        
        if hasattr(user_config, 'DEFAULT_MODELS'):
            config["default_models"].update(user_config.DEFAULT_MODELS)
            
        if hasattr(user_config, 'TOOLS_DIR'):
            config["tools_dir"] = user_config.TOOLS_DIR
            
        if hasattr(user_config, 'GENERATED_IMAGES_DIR'):
            config["generated_images_dir"] = user_config.GENERATED_IMAGES_DIR
            
        if hasattr(user_config, 'GENERATED_AUDIO_DIR'):
            config["generated_audio_dir"] = user_config.GENERATED_AUDIO_DIR
            
        return config
        
    except Exception as e:
        print(f"Error loading config from {config_path}: {e}", file=sys.stderr)
        print("Using default configuration", file=sys.stderr)
        return {"models": DEFAULT_MODELS}

def ensure_config_file():
    """Create default config file if it doesn't exist."""
    config_path = get_config_path()
    if not config_path.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)
        # Get the path to default_config.py
        default_config_path = Path(__file__).parent / 'default_config.py'
        if default_config_path.exists():
            # Copy the default config file
            shutil.copy(default_config_path, config_path)
        else:
            # Fallback if default_config.py isn't found
            with open(config_path, 'w') as f:
                f.write('''"""User configuration for smai."""
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
''')

# Create config file if it doesn't exist
ensure_config_file()

# Load configuration when module is imported
CONFIG = load_user_config()
