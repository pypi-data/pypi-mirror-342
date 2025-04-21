import os
import google.generativeai as genai
from pathlib import Path
import re
from .env_var import set_gemini_api_key

def split_path(path):
    return re.split(r'[\\/]', path)

home_path = Path.home()
username = split_path(str(home_path))[-1]

# 👇 Get the current terminal working directory (where the script is run from)
current_working_directory = os.getcwd()

from .prompts import (
    get_commandline_prompt,
    check_command_safety_prompt,
    get_message_prompt,
)

def configure_gemini_api():
    api_key = set_gemini_api_key()
    genai.configure(api_key=api_key)

def generate_shell_command(user_command, gemini_api_key, gemini_model_config):
    formatted_prompt = (
        "Convert the following natural language request into a valid Windows shell command."
        " Respond with ONLY the shell command—no explanations, no headers, no additional text."
        " Ensure the command is fully executable as-is."
        " Use absolute paths only, and do not include environment variables like %USERPROFILE% or %APPDATA%."
        f" Assume the username is '{username}' and explicitly replace all occurrences of %USERPROFILE% or %APPDATA% with '{home_path}'."
        " Ensure the command is optimized for Windows and follows best shell scripting practices."
        " Expand wildcards (e.g., '*.txt') correctly so they match files when executed in a shell."
        " Avoid interactive commands that require user input; commands should execute autonomously."
        " Prefer using built-in Windows utilities and avoid non-default software dependencies."
        " Format the response strictly as a single-line command with no line breaks."
        f" Ensure the generated command explicitly sets the working directory to '{current_working_directory}' before running the command."
        " If the command creates a folder, verify that the folder is created in the correct location."
        " For root access, ensure the command is run from the 'C:\\Windows\\System32\\' directory or with elevated permissions."
        f" Otherwise, commands should run from the user's directory, assumed to be '{home_path}'."
        "\n\n"
        f"Request: {user_command}\nShell Command:"
    )



    configure_gemini_api()
    model = genai.GenerativeModel(gemini_model_config["model_name"])
    response = model.generate_content(formatted_prompt)

    # Debugging: Print raw response
    # print(f"DEBUG: Raw Gemini Response: {response}")

    # Extract the shell command from response
    try:
        shell_command = response.candidates[0].content.parts[0].text.strip()
        # print(f"DEBUG: Extracted shell command: {shell_command}")
    except AttributeError:
        # print("ERROR: Gemini API response structure unexpected!")
        shell_command = None  # Set it explicitly to None for debugging

    # Validate the generated command
    if shell_command is None or shell_command == "":
        # print("ERROR: Gemini failed to generate a valid shell command.")
        shell_command = "echo 'Error: Unable to generate a shell command'"

    return shell_command





def is_command_safe(shell_command, gemini_api_key, gemini_model_config):
    configure_gemini_api()

    formatted_prompt = check_command_safety_prompt.format(command=shell_command)

    model = genai.GenerativeModel(gemini_model_config["model_name"])  # Corrected
    response = model.generate_content(formatted_prompt)  # Correct method

    safety_result = response.text.strip() if response and hasattr(response, 'text') else "Error analyzing command"
    return safety_result

def get_result_analysis(result_text):
    """
    Analyzes the result text and determines if the command execution was successful or not.
    This is a placeholder function, modify as needed.
    """
    if "error" in result_text.lower():
        return "Warning: The generated command may cause issues."
    return "The command seems valid."
