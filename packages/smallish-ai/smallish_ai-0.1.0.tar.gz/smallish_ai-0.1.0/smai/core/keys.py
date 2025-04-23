import os
import keyring
import getpass
from typing import Optional
from .db import add_api_key, remove_api_key, get_api_keys

def set_key(key_name: str, key_value: Optional[str] = None) -> None:
    """Store an API key in the system keyring.
    
    Args:
        key_name: Name of the key (e.g., 'OPENAI_API_KEY')
        key_value: Optional key value. If not provided, will prompt user.
    """
    if key_value is None:
        key_value = getpass.getpass(f"Please enter the value for {key_name}: ")
    
    keyring.set_password("smai", key_name, key_value)
    add_api_key(key_name)
    print(f"{key_name} has been set.")

def remove_key(key_name: str) -> None:
    """Remove an API key from the system keyring.
    
    Args:
        key_name: Name of the key to remove
    """
    try:
        keyring.delete_password("smai", key_name)
        remove_api_key(key_name)
        print(f"{key_name} has been removed.")
    except keyring.errors.PasswordDeleteError:
        print(f"No key named {key_name} was found.")

def load_keys() -> None:
    """Load all stored API keys into environment variables."""
    key_names = get_api_keys()
    
    for key_name in key_names:
        key_value = keyring.get_password("smai", key_name)
        if key_value:
            os.environ[key_name] = key_value
