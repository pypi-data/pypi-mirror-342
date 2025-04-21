import os
import platform
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
API_KEY_FILENAME = os.path.join(BASE_DIR, "gemini_api_key.txt")
# print(API_KEY_FILENAME)
# API_KEY_FILENAME = "gemini_api_key.txt"
ENV_VAR_NAME = "GEMINI_API_KEY"

def is_env_var_set(var_name):
    """Check if the environment variable is already set and return its value."""
    return os.getenv(var_name)

def read_api_key_from_file(filename):
    """Read the API key from a local text file."""
    full_path = os.path.abspath(filename)
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            key = file.read().strip()
            if key:
                print(f"📄 Found API key in text file. {full_path}")
                return key
    return None

def save_api_key_to_file(filename, api_key):
    """Save the API key to a local text file and print the full path."""
    with open(filename, 'w') as file:
        file.write(api_key)
    print(f"💾 API key saved to: {filename}")


def get_user_input(prompt):
    """Get input from the user and ensure it's not empty."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("⚠️ Value cannot be empty. Please enter again.")

def set_env_var_temp(var_name, var_value):
    """Set an environment variable temporarily for the current session."""
    os.environ[var_name] = var_value
    print(f"✅ {var_name} set for the current session.")

def set_env_var_permanent_linux(var_name, var_value):
    """Set an environment variable permanently on Linux/macOS."""
    bashrc_path = os.path.expanduser("~/.bashrc")
    env_file_path = "/etc/environment"

    try:
        # Append to ~/.bashrc
        with open(bashrc_path, "a") as f:
            f.write(f'\nexport {var_name}="{var_value}"\n')

        # Append to /etc/environment
        with open(env_file_path, "a") as f:
            f.write(f'\n{var_name}="{var_value}"\n')

        print(f"✅ {var_name} permanently added to ~/.bashrc and /etc/environment.")
    except PermissionError:
        print("⚠️ Permission denied: Run this script with sudo to modify system-wide environment variables.")

def set_env_var_permanent_windows(var_name, var_value):
    """Set an environment variable permanently on Windows using setx."""
    try:
        subprocess.run(["setx", var_name, var_value], shell=True, check=True)
        print(f"✅ {var_name} permanently added to Windows environment.")
    except Exception as e:
        print(f"⚠️ Error setting Windows environment variable: {e}")

def set_gemini_api_key():
    """Check and set the GEMINI_API_KEY variable globally, returning the key."""
    # Check if the environment variable is already set
    existing_key = is_env_var_set(ENV_VAR_NAME)
    if existing_key:
        return existing_key

    # Check the text file fallback
    file_key = read_api_key_from_file(API_KEY_FILENAME)
    if file_key:
        set_env_var_temp(ENV_VAR_NAME, file_key)
        return file_key

    # Ask user for the key if not found
    api_key = get_user_input("Enter your GEMINI API Key: ")

    # Save to file
    save_api_key_to_file(API_KEY_FILENAME, api_key)

    # Set temporarily for this session
    set_env_var_temp(ENV_VAR_NAME, api_key)

    # Set permanently based on the OS
    if platform.system() == "Windows":
        set_env_var_permanent_windows(ENV_VAR_NAME, api_key)
    else:
        set_env_var_permanent_linux(ENV_VAR_NAME, api_key)

    return api_key

# Example usage
if __name__ == "__main__":
    api_key = set_gemini_api_key()
    print(f"🔑 Your GEMINI API Key: {api_key}")
