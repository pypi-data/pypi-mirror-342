import subprocess
import os

# Define the path to store the log file
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "failed_commands.txt")

# List of test commands (natural language input) and their expected outputs
test_cases = [
    {
        "command": "open the terminal",
        "expected_output": "Terminal opened"  # Adjust with what vigi returns when opening a terminal
    },
    {
        "command": "list all files",
        "expected_output": "file1.txt\nfile2.txt\nfile3.txt"  # Replace with actual files in your directory
    },
    {
        "command": "create a new directory named test_dir",
        "expected_output": "Directory test_dir created"  # Adjust with what vigi returns upon directory creation
    },
    {
        "command": "check disk usage",
        "expected_output": "Disk usage: 50%"  # Adjust with actual disk usage info from your system
    },
    {
        "command": "remove the test_dir directory",
        "expected_output": "Directory test_dir removed"  # Adjust with vigi's response after removing directory
    },
    {
        "command": "list all processes",
        "expected_output": "process1\nprocess2\nprocess3"  # Adjust with process names running on your system
    },
    {
        "command": "show the current date and time",
        "expected_output": "Current date and time: "  # You can expect something like "Current date and time: YYYY-MM-DD HH:MM:SS"
    }
]

# Function to clean the output by removing unwanted lines
def clean_output(output):
    cleaned_output = []
    for line in output.splitlines():
        # Filter out the lines with unnecessary information (e.g., Gemini, logging, etc.)
        if "Gemini" not in line and "command:" not in line:  # adjust as needed
            cleaned_output.append(line)
    return "\n".join(cleaned_output)

# Function to run a command using subprocess
def run_vigi_command(command):
    try:
        print("THIS COMMAND     ",f'\"{command}\"')
        # Run the command in the terminal and capture the output
        result = subprocess.run(
            ["vigi", f'\"{command}\"'], text=True, capture_output=True, check=True
        )
        return result.stdout  # Return the output
    except subprocess.CalledProcessError as e:
        # If an error occurs, return the error output
        return e.stderr

# Function to compare actual output with expected output
def test_command(command, expected_output):
    actual_output = run_vigi_command(command)
    cleaned_actual_output = clean_output(actual_output)

    if expected_output not in cleaned_actual_output:
        # Log failed command and output to the desktop file
        with open(desktop_path, "a") as f:
            f.write(f"Failed Command: {command}\n")
            f.write(f"Actual Output: {cleaned_actual_output}\n\n")
        return False
    return True

# Test the commands and track the success rate
failed_commands = []
for test_case in test_cases:
    command = test_case["command"]
    expected_output = test_case["expected_output"]
    
    success = test_command(command, expected_output)
    if not success:
        failed_commands.append(command)

# Calculate success rate
success_rate = (len(test_cases) - len(failed_commands)) / len(test_cases) * 100

print(f"Test completed. Success rate: {success_rate}%")
print(f"Failed commands are logged at: {desktop_path}")
