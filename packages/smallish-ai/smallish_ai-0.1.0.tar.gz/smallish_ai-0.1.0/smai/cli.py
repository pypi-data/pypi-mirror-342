#!/usr/bin/env python3

import click
import sys
import os
import json
import logging
import re
from typing import List, Optional, Dict, Any, Tuple
import warnings
import inspect
from typing import Union
from litellm import completion, stream_chunk_builder
import litellm.exceptions

from .core.keys import set_key, remove_key, load_keys
from .core.conversation import Conversation
from .core.config import CONFIG
from .core.tools import get_available_tools, get_tools_for_model, execute_tool
from .core.image import is_image_file, is_pdf_file, encode_image, generate_image, get_pdf_message, get_image_message
from .core.audio import is_audio_file, process_audio_input, transcribe_audio, generate_speech
from .core.inputs import process_predefined_inputs

DEFAULT_MODEL = CONFIG["default_models"]["text"]
DEFAULT_IMAGE_MODEL = CONFIG["default_models"]["image"]
DEFAULT_AUDIO_MODEL = CONFIG["default_models"]["audio"]
# TODO: Remove this explicit check, see if litellm has a way to figure this out.
AUDIO_INPUT_MODELS = ["whisper"]  # Models that support audio input

def process_file_input(input_item: str, model: str) -> dict:
    """Process a single file input."""
    if is_pdf_file(input_item):
        return get_pdf_message(input_item, model)
    elif is_image_file(input_item):
        return get_image_message(input_item)
    elif is_audio_file(input_item) and model in AUDIO_INPUT_MODELS:
        return process_audio_input(input_item, model)
    else:
        with open(input_item, 'r') as file:
            return {"type": "text", "text": file.read()}

def process_inputs(inputs: List[str], model: str) -> List[dict]:
    """Process a list of inputs into a format suitable for AI model consumption."""
    messages = []
    processed_inputs = process_predefined_inputs(inputs)
    
    # Process file and text inputs
    messages.extend(
        process_file_input(item, model) if os.path.isfile(item)
        else {"type": "text", "text": item}
        for item in processed_inputs
    )
    
    # Add stdin input if available
    if not sys.stdin.isatty():
        stdin_input = sys.stdin.read().strip()
        if stdin_input:
            messages.append({"type": "text", "text": stdin_input})
    
    return messages

def handle_streaming_response(response) -> Tuple[str, dict, Optional[list]]:
    """Handle streaming response from the model."""
    full_response = ""
    chunks = []
    
    for chunk in response:
        chunks.append(chunk)
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            full_response += content

    response = stream_chunk_builder(chunks)
    response_message = response.choices[0].message
    return full_response, response_message, response_message.tool_calls

def extract_key_name(error_msg: str) -> Optional[str]:
    """Extract API key name from authentication error message."""
    key_match = re.search(r'`([^`]+)`', error_msg)
    if key_match:
        return key_match.group(1)
    return None

def handle_auth_error(auth_err: litellm.exceptions.AuthenticationError) -> None:
    """Handle authentication errors by providing helpful guidance."""
    error_msg = str(auth_err)
    logging.error(f"Authentication error: {error_msg}")
    print(f"Authentication error: {error_msg}")
    
    # Extract key name from error message if available
    key_name = extract_key_name(error_msg)
    if key_name:
        print(f"\nMissing or invalid API key: {key_name}")
    
    print("\nTo set your API key, you can:")
    if key_name:
        print(f"1. Use the --set-key command: smai --set-key {key_name}")
    else:
        print("1. Use the --set-key command: smai --set-key MODEL_PROVIDER")
    print(f"2. Set the {key_name or 'API_KEY'} environment variable")
    sys.exit(1)


# --- Tool Handling ---

def handle_tool_calls(tool_calls: list, interactive_tools: bool) -> List[dict]:
    """Process tool calls and return tool responses."""
    tool_responses = []
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        
        logging.info(f"Tool call requested: {function_name} with args: {function_args}")
        
        tool_response = execute_tool(function_name, function_args, interactive_tools)
        logging.info(f"Tool response: {tool_response}")
        
        tool_responses.append({
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": function_name,
            "content": tool_response
        })
    return tool_responses

def generate_text(conversation: Conversation) -> Tuple[str, Conversation]:
    """Generate text using the specified AI model with optional tool usage."""
    try:
        model = conversation.model
        tools = conversation.tools
        
        model_tools = get_tools_for_model(tools) if tools else None
        logging.info(f"Starting generation with model: {model}, tools: {tools}, streaming: {conversation.streaming}")
        
        while True:
            try:
                response = completion(
                    model=model,
                    messages=conversation.model_messages,
                    tools=model_tools,
                    tool_choice="auto" if tools else None,
                    stream=conversation.streaming,
                    **conversation.kwargs
                )
            except litellm.exceptions.AuthenticationError as auth_err:
                handle_auth_error(auth_err)

            if conversation.streaming:
                full_response, response_message, tool_calls = handle_streaming_response(response)
            else:
                response_message = response.choices[0].message
                full_response = response_message.content
                print(full_response, end="", flush=True)
                tool_calls = response_message.tool_calls

            conversation.add_message(response_message.dict())

            if tool_calls:
                tool_responses = handle_tool_calls(tool_calls, conversation.interactive_tools)
                for tool_response in tool_responses:
                    conversation.add_message(tool_response)
            else:
                break

        print()  # New line at the end
        return full_response, conversation
        
    except Exception as e:
        logging.error(f"Error in generate_text: {str(e)}", exc_info=True)
        print(f"An error occurred: {str(e)}")
        return "", conversation

def transcribe_audio_wrapper(conversation: Conversation) -> str:
    """Transcribe audio using the model specified in the conversation."""
    model = conversation.model
    
    # Find the user message
    user_messages = [msg for msg in conversation.model_messages if msg["role"] == "user"]
    if not user_messages:
        raise ValueError("No user message found in conversation")
    
    # Get the content of the last user message
    user_content = user_messages[-1]["content"]
    
    # Find the audio file
    audio_file = None
    for msg in user_content:
        if msg["type"] == "audio_input":
            audio_file = msg["original_file"]
            break
    
    if not audio_file:
        raise ValueError("No audio file found in messages")
    
    prompt = ""  # Could extract a prompt from text messages if needed
    
    try:
        output = transcribe_audio(model, audio_file, prompt)
        return output
    except litellm.exceptions.AuthenticationError as auth_err:
        handle_auth_error(auth_err)

def get_user_message_text(conversation: Conversation) -> str:
    """Extract text from the last user message in the conversation."""
    # Find the user message
    user_messages = [msg for msg in conversation.model_messages if msg["role"] == "user"]
    if not user_messages:
        raise ValueError("No user message found in conversation")
    
    # Get the content of the last user message
    user_content = user_messages[-1]["content"]
    
    # Extract text from messages
    return " ".join([msg["text"] for msg in user_content if msg["type"] == "text"])

def generate_speech_wrapper(conversation: Conversation, output_file: Optional[str] = None) -> None:
    """Generate speech from text using the specified text-to-speech model."""
    model = conversation.model
    
    text = get_user_message_text(conversation)
    
    try:
        audio_file = generate_speech(model, text, output_file=output_file)
        # Add an assistant message to the conversation with the audio file path.
        conversation.add_message({"role": "assistant", "content": f"{audio_file}"})
        print(f"{audio_file}")
    except litellm.exceptions.AuthenticationError as auth_err:
        handle_auth_error(auth_err)
    except Exception as e:
        logging.error(f"Error in generate_speech_wrapper: {str(e)}", exc_info=True)
        print(f"An error occurred while generating speech: {str(e)}")

def generate_image_wrapper(conversation: Conversation, output_file: Optional[str] = None) -> None:
    """Generate an image using the specified image generation model."""
    model = conversation.model
    
    prompt = get_user_message_text(conversation)
    
    try:
        filename = generate_image(model, prompt, output_file)
        # Add an assistant message to the conversation with the image path.
        conversation.add_message({"role": "assistant", "content": f"{filename}"})
        print(f"{filename}")
    except litellm.exceptions.AuthenticationError as auth_err:
        handle_auth_error(auth_err)


# --- Argument Processing ---

def process_model_kwargs(ctx_args: List[str]) -> Dict[str, Any]:
    """Process extra command line arguments from the context into model parameters."""
    kwargs = {}
    i = 0
    while i < len(ctx_args):
        arg = ctx_args[i]
        if arg.startswith('--'):
            param_part = arg[2:]  # Remove '--'

            # Handle --param=value format
            if '=' in param_part:
                param, value = param_part.split('=', 1)
                i += 1
            # Handle --param value format
            elif i + 1 < len(ctx_args) and not ctx_args[i + 1].startswith('--'):
                param = param_part
                value = ctx_args[i + 1]
                i += 2
            # Handle boolean flags like --param
            else:
                param = param_part
                value = "true" # Assume boolean flag if no value follows
                i += 1
            
            # Check if parameter exists in completion function signature
            sig = inspect.signature(completion)
            if param not in sig.parameters:
                logging.fatal(f"Parameter '{param}' is not supported by the completion function")
                logging.fatal(f"Supported parameters: {', '.join(sig.parameters.keys())}")
                sys.exit(1)
            
            param_type = sig.parameters[param]

            # Get the base type, handling Optional types
            type_hint = param_type.annotation
            if hasattr(type_hint, "__origin__") and type_hint.__origin__ is Union:
                # Handle Optional types (Union[type, NoneType])
                base_type = type_hint.__args__[0]
            else:
                base_type = type_hint

            # Convert value to correct type
            try:
                if value.lower() == 'none':
                    kwargs[param] = None
                elif base_type == bool:
                    kwargs[param] = value.lower() in ('true', '1', 'yes', 'y')
                elif base_type == float:
                    kwargs[param] = float(value)
                elif base_type == int:
                    kwargs[param] = int(value)
                elif base_type == str:
                    kwargs[param] = value
                elif base_type == dict:
                    try:
                        kwargs[param] = json.loads(value)
                    except json.JSONDecodeError:
                        logging.fatal(f"Invalid JSON format for parameter '{param}': {value}")
                        sys.exit(1)
                else:
                    logging.fatal(f"Unsupported parameter type for '{param}': {base_type}")
                    sys.exit(1)
            except ValueError:
                logging.fatal(f"Invalid value for parameter '{param}': {value}")
                sys.exit(1)
        else:
            # Skip non -- arguments if any slip through somehow
            logging.warning(f"Skipping unexpected argument: {arg}")
            i += 1
            continue

    return kwargs


# --- Main CLI Command ---

@click.command(
    context_settings=dict(
        ignore_unknown_options=True,  # Allow unknown options like --temperature
        allow_extra_args=True         # Capture extra args for model kwargs
    ),
    help="""Small AI (smai) - Use various generative AI models from the command line.

This tool allows you to interact with various AI models for:
- Text generation (default)
- Image generation
- Audio transcription
- Text-to-speech conversion

Basic Usage:
    smai "Your prompt here"
    echo "Your prompt" | smai
    smai input.txt""",
    epilog="""Examples:
    # Basic text generation
    smai "Tell me a joke"

    # Use a specific model
    smai -m gpt-4 "Explain quantum computing"

    # Pass model-specific parameters (like temperature)
    smai -m gpt-4 --temperature 0.5 "Write a creative story"

    # Generate an image
    smai -m dall-e-3 -o image.png "A sunset over mountains"

    # Use tools
    smai -t calculator,weather "How much colder is Paris than SF right now?"

    # Prompt user before using tools
    smai -it calculator,weather "Let's do some calculations"

    # Transcribe audio
    smai -m whisper input.mp3

    # Generate speech
    smai -m tts -o output.mp3 "Text to convert to speech"

    # Set an API key (prompts for value if not provided)
    smai --set-key OPENAI_API_KEY

    # Set an API key with value
    smai --set-key OPENAI_API_KEY sk-xxxxxxxx

    # Remove an API key
    smai --remove-key OPENAI_API_KEY
    """
)
@click.option("-m", "--model", help="AI model to use.")
@click.option("-o", "--output", help="Output file/directory for generated files.")
@click.option("-i", "--image", is_flag=True, help="Generate an image (uses default image model).")
@click.option("-a", "--audio", is_flag=True, help="Generate audio (uses default audio model).")
@click.option("-t", "--tools", help="Comma-separated tools to use without prompting.")
@click.option("-it", "--interactive-tools", help="Comma-separated tools to use with interactive prompting.")
@click.option("--no-streaming", is_flag=True, default=False, help="Disable streaming mode for text generation.")
@click.option("-s", "--system", help="Set a system prompt for text generation.")
@click.option("-c", "--continue", "continue_conversation", is_flag=True, help="Continue the most recent conversation.")
@click.option("--set-key", "set_key_name", metavar="KEY_NAME", help="Set an API key.")
@click.option("--remove-key", "remove_key_name", metavar="KEY_NAME", help="Remove an API key.")
@click.argument("inputs", nargs=-1)
@click.pass_context
def main(ctx, model, output, image, audio, tools, interactive_tools, no_streaming, system, continue_conversation, set_key_name, remove_key_name, inputs):
    """Main entry point for the smai command-line interface, powered by Click."""
    # Load API keys from keyring
    load_keys()

    # Process model kwargs from extra args captured by click context
    kwargs = process_model_kwargs(ctx.args)

    # Handle key management commands first
    if set_key_name:
        # 'inputs' will capture the key value if provided after the key name
        key_value = inputs[0] if inputs else None
        set_key(set_key_name, key_value)
        sys.exit(0)
    elif remove_key_name:
        remove_key(remove_key_name)
        sys.exit(0)

    # Check for mutually exclusive tool options
    if tools and interactive_tools:
        logging.fatal("Options --tools (-t) and --interactive-tools (-it) are mutually exclusive.")
        sys.exit(1)

    # Check if input is provided either via arguments or stdin
    if not inputs and sys.stdin.isatty():
        click.echo(ctx.get_help()) # Show help if no input and not piping
        sys.exit(1)

    try:
        # Process inputs (including stdin if available)
        messages = process_inputs(list(inputs), model) # Convert tuple to list

        # Determine which tools to use and if interactive
        current_tools = None
        is_interactive = False
        if tools:
            current_tools = tools.split(',')
        elif interactive_tools:
            current_tools = interactive_tools.split(',')
            is_interactive = True

        # Validate tools if specified
        if current_tools:
            available_tools = get_available_tools()
            invalid_tools = [tool for tool in current_tools if tool not in available_tools]
            if invalid_tools:
                logging.fatal(f"Invalid tool(s) specified: {', '.join(invalid_tools)}")
                logging.fatal(f"Available tools are: {', '.join(available_tools)}")
                sys.exit(1)

        # Determine appropriate model if not explicitly set
        effective_model = model
        if not effective_model:
            if image:
                effective_model = DEFAULT_IMAGE_MODEL
            elif audio:
                effective_model = DEFAULT_AUDIO_MODEL
            else:
                effective_model = DEFAULT_MODEL

        # Determine output type
        output_type = "text"
        if image and audio:
            logging.fatal("Cannot enable both --image (-i) and --audio (-a) at the same time.")
            sys.exit(1)
        elif image:
            output_type = "image"
        elif audio:
            output_type = "audio"

        # Initialize or continue conversation
        if continue_conversation:
            # TODO: Restrict continuation based on output_type?
            conversation = Conversation.get_latest()
            if not conversation:
                logging.fatal("No previous conversation found to continue.")
                sys.exit(1)
            # Update conversation with potentially new parameters? (e.g., model, tools) - For now, just continue as is.
            logging.info(f"Continuing conversation ID: {conversation.id}")
        else:
            # Create a new conversation object
            conversation = Conversation(
                model=effective_model,
                tools=current_tools,
                interactive_tools=is_interactive,
                streaming=not no_streaming,
                output_type=output_type,
                kwargs=kwargs
            )

            # Add system prompt if provided
            if system:
                # Process potential predefined inputs in system prompt
                processed_system_prompt = process_predefined_inputs([system])[0]
                conversation.add_message({"role": "system", "content": processed_system_prompt})

        # Add user message(s) to the conversation
        # If continuing, this adds the new prompt to the existing conversation
        conversation.add_message({"role": "user", "content": messages})

        # --- Execute appropriate action based on flags/input ---

        # Check if the primary input is a single audio file for transcription
        is_single_audio_input = (
            len(messages) == 1 and
            messages[0]["type"] == "audio_input" and
            effective_model in AUDIO_INPUT_MODELS # Ensure model supports audio input
        )

        if is_single_audio_input and not image and not audio: # Prioritize transcription if model supports it
             output_text = transcribe_audio_wrapper(conversation)
             print(output_text)
             # TODO: Should we save the conversation for transcription?
        elif image: # Handle image generation
            generate_image_wrapper(conversation, output)
            conversation.save() # Save conversation state
        elif audio: # Handle audio generation (TTS)
            generate_speech_wrapper(conversation, output)
            conversation.save() # Save conversation state
        else: # Default to text generation
            _, updated_conversation = generate_text(conversation)
            updated_conversation.save() # Save conversation state after generation

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}", exc_info=True)
        print(f"\nAn error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
