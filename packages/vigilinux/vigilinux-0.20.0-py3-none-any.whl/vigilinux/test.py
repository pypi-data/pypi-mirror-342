import subprocess
import os

command = "what is the time right now"
result = subprocess.run(
            ["python","main.py", f'\"{command}\"'], text=True, capture_output=True, check=True
        )
print(result)