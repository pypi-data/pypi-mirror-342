import os
import subprocess
from typing import Optional

def get_predefined_input(input_name: str) -> Optional[str]:
    """
    Retrieve the predefined input for the given input name.
    Returns None if no predefined input is found.
    """
    config_dir = os.path.expanduser("~/.config/smai/inputs")
    md_file = os.path.join(config_dir, f"{input_name}.md")
    executable_file = os.path.join(config_dir, input_name)

    if os.path.isfile(md_file):
        with open(md_file, 'r') as f:
            return f.read().strip()
    elif os.path.isfile(executable_file) and os.access(executable_file, os.X_OK):
        try:
            result = subprocess.run([executable_file], capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error executing predefined input '{input_name}': {e}")
            return None
    else:
        return None

def process_predefined_inputs(inputs: list) -> list:
    """
    Process a list of inputs, replacing any predefined inputs with their content.
    """
    processed_inputs = []
    for input_item in inputs:
        predefined_content = get_predefined_input(input_item)
        if predefined_content is not None:
            processed_inputs.append(predefined_content)
        else:
            processed_inputs.append(input_item)
    return processed_inputs
