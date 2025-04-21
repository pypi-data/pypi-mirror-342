import os
import platform
import subprocess

def is_env_var_set(var_name):
    """Check if the environment variable is already set and return its value."""
    return os.getenv(var_name)

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
        # Append to ~/.bashrc (User level)
        with open(bashrc_path, "a") as f:
            f.write(f'\nexport {var_name}="{var_value}"\n')

        # Append to /etc/environment (System-wide, requires sudo)
        with open(env_file_path, "a") as f:
            f.write(f'\n{var_name}="{var_value}"\n')

        print(f"✅ {var_name} permanently added to ~/.bashrc and /etc/environment. Restart or run `source ~/.bashrc` to apply.")
    except PermissionError:
        print("⚠️ Permission denied: Run this script with sudo to modify system-wide environment variables.")

def set_env_var_permanent_windows(var_name, var_value):
    """Set an environment variable permanently on Windows using setx."""
    try:
        subprocess.run(["setx", var_name, var_value], shell=True, check=True)
        print(f"✅ {var_name} permanently added to Windows environment. Restart your terminal or system to apply.")
    except Exception as e:
        print(f"⚠️ Error setting Windows environment variable: {e}")

def set_gemini_api_key():
    """Check and set the GEMINI_API_KEY variable globally, returning the key."""
    var_name = "GEMINI_API_KEY"

    # Check if the variable is already set
    existing_key = is_env_var_set(var_name)
    if existing_key:
        # print(f"✅ {var_name} is already set.")
        return existing_key  # Return the existing key

    # Ask the user for the API key
    api_key = get_user_input("Enter your GEMINI API Key: ")

    # Set temporarily for this session
    set_env_var_temp(var_name, api_key)

    # Set permanently based on the OS
    if platform.system() == "Windows":
        set_env_var_permanent_windows(var_name, api_key)
    else:  # Linux/macOS
        set_env_var_permanent_linux(var_name, api_key)

    return api_key  # Return the newly entered key

# Example usage
if __name__ == "__main__":
    var_name = "GEMINI_API_KEY"
    # Check if the variable is already set
    existing_key = is_env_var_set(var_name)
    
    print(existing_key)
    # api_key = set_gemini_api_key()
    # print(f"🔑 Your GEMINI API Key: {api_key}")
