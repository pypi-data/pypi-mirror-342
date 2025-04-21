import json
import importlib.resources
import os

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def load_settings():
 

    
    # Open the settings file and load its contents
 
    settings ={
    "speak_commands": False,
    "command_execution_confirmation": False,
    "use_colors": True,
    "security_check": True,
    "gemini_model_config": {
      "model_name": "gemini-1.5-pro",
      "temperature": 0.7,
      "max_tokens": 100
    }
}


    
    return settings




# Load settings
settings = load_settings()


