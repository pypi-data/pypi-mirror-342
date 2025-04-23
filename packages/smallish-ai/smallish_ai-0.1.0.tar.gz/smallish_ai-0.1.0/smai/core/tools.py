import os
import json
import subprocess
from typing import List, Dict, Any
from .config import CONFIG

TOOLS_DIR = CONFIG["tools_dir"]

def get_available_tools() -> List[str]:
    """Return a list of available tool names."""
    if not os.path.exists(TOOLS_DIR):
        return []
    return [d for d in os.listdir(TOOLS_DIR) if os.path.isdir(os.path.join(TOOLS_DIR, d))]

def get_tool_description(tool_name: str) -> Dict[str, Any]:
    """Read and return the tool description from the JSON file."""
    desc_path = os.path.join(TOOLS_DIR, tool_name, "description.json")
    try:
        with open(desc_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def execute_tool(tool_name: str, args: Dict[str, Any], interactive: bool = False) -> str:
    """Execute the specified tool with given arguments as environment variables."""
    tool_path = os.path.join(TOOLS_DIR, tool_name, tool_name)
    # Check if the tool exists and is executable
    if not os.path.exists(tool_path) or not os.access(tool_path, os.X_OK):
        return f"Error: Tool '{tool_name}' not found or not executable."
    
    if interactive:
        print(f"\nModel wants to use tool: {tool_name}")
        print(f"Arguments: {args}")
        approval = input("Approve tool use? (y/n): ").lower().strip()
        if approval != 'y':
            return "Tool use not approved."
    else:
        print(f"\n\nExecuting tool '{tool_name}' with arguments: {args}\n\n")
    
    # Prepare environment variables
    env = os.environ.copy()
    for key, value in args.items():
        env[key] = str(value)
    
    try:
        result = subprocess.run([tool_path], capture_output=True, text=True, check=True, env=env)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error executing tool '{tool_name}': {e.stderr.strip()}"

def get_tools_for_model(tools: List[str]) -> List[Dict[str, Any]]:
    """Prepare tool descriptions for the model."""
    return [desc for tool in tools if (desc := get_tool_description(tool))]
