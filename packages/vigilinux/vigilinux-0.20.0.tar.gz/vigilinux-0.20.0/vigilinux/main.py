#!/usr/bin/env python3
import os
import re
import sys
import time
import threading
import subprocess
import itertools
import platform
from pathlib import Path

from dotenv import load_dotenv
from .config import settings, Colors
from .openai_api import generate_shell_command, is_command_safe
from .utils import colorize
from .env_var import set_gemini_api_key
from .voice_recog import audio_to_text

# Constants
MAX_LOOPS = 10           # How many times to ask Gemini before giving up
TIMEOUT = 10000          # Seconds before killing a hanging process

home_path = Path.home()


class LoadingDots:
    def __init__(self, message="Processing"):
        self.message = message
        self.running = False
        self.thread = None
        self.spinner = itertools.cycle(['⣾','⣽','⣻','⢿','⡿','⣟','⣯','⣷'])

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.start()

    def _animate(self):
        while self.running:
            spin_char = next(self.spinner)
            sys.stdout.write(f'\r{self.message} {spin_char}')
            sys.stdout.flush()
            time.sleep(0.1)

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        sys.stdout.write('\r' + ' ' * (len(self.message) + 2) + '\r')
        sys.stdout.flush()


def load_env_vars():
    load_dotenv()
    return os.getenv("GEMINI_API_KEY")


def read_config():
    return (
        settings["command_execution_confirmation"],
        settings["security_check"],
        settings["gemini_model_config"],
    )


def recognize_operating_system():
    return platform.system()


def read_user_command():
    return " ".join(sys.argv[1:])


def execute_command_with_interaction(shell_command, timeout=TIMEOUT):
    """
    Runs shell_command, prints output live, handles simple y/n prompts,
    and returns (stdout, stderr). Raises CalledProcessError on non-zero exit.
    """
    print(colorize(f"EXECUTING: {shell_command}", Colors.OKGREEN))
    proc = subprocess.Popen(
        shell_command, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        stdin=subprocess.PIPE, text=True
    )

    stdout_lines, stderr_lines = [], []

    def reader(stream, accumulator):
        for line in iter(stream.readline, ""):
            accumulator.append(line)
            print(line.rstrip())
            # if interactive prompt detected:
            if any(tok in line.lower() for tok in ("continue?", "yes/no", "y/n")):
                resp = input("🔹 Enter response: ") + "\n"
                proc.stdin.write(resp)
                proc.stdin.flush()

    t_out = threading.Thread(target=reader, args=(proc.stdout, stdout_lines))
    t_err = threading.Thread(target=reader, args=(proc.stderr, stderr_lines))
    t_out.start(); t_err.start()

    start = time.time()
    while proc.poll() is None:
        if time.time() - start > timeout:
            print(colorize("⏳ Timeout reached! Terminating process...", Colors.FAIL))
            proc.terminate()
            return "".join(stdout_lines), "".join(stderr_lines) + "\n[Killed due to timeout]"

    t_out.join(); t_err.join()
    ret = proc.wait()
    stdout = "".join(stdout_lines)
    stderr = "".join(stderr_lines)
    if ret != 0:
        raise subprocess.CalledProcessError(ret, shell_command, output=stdout, stderr=stderr)
    return stdout, stderr


def ask_gemini_next_step(user_request, shell_command, stdout, stderr,
                         gemini_api_key, gemini_model_config):
    """
    Sends the full output back to Gemini and asks:
      - Line 1: DONE or CONTINUE
      - Line 2: (if CONTINUE) the next exact shell command
    Also instructs Gemini to install missing packages if needed.
    """
    prompt = (
        f"User's original request: {user_request}\n"
        f"Command I just ran: {shell_command}\n"
        f"---- STDOUT ----\n{stdout}\n"
        f"---- STDERR ----\n{stderr}\n\n"
        "Based on this output, first reply with exactly 'DONE' if the user's request is complete, "
        "or 'CONTINUE' if more steps are required. "
        "If you say 'CONTINUE', on the next line provide the exact shell command to run to proceed. "
        "If any required package or command is missing, include the installation command (for example, "
        "`sudo apt-get install <package> -y`, `brew install <package>`, or `choco install <package> -y`) "
        "before the next action."
    )
    response = generate_shell_command(prompt, gemini_api_key, gemini_model_config).strip()
    lines = [l.strip() for l in response.splitlines() if l.strip()]
    if not lines:
        raise RuntimeError("Gemini returned no actionable output.")
    status = lines[0].upper()
    next_cmd = lines[1] if len(lines) > 1 else None
    return status, next_cmd


def execute_with_gemini_loop(user_command,
                             initial_command,
                             security_check,
                             gemini_api_key,
                             gemini_model_config,
                             command_execution_confirmation,
                             operating_system):
    """
    Main loop: run a command, capture its output, ask Gemini if we're DONE or need to CONTINUE.
    """
    shell_command = initial_command

    for attempt in range(MAX_LOOPS):
        try:
            stdout, stderr = execute_command_with_interaction(shell_command)
        except subprocess.CalledProcessError as e:
            stdout = e.output or ""
            stderr = e.stderr or str(e)

        status, next_cmd = ask_gemini_next_step(
            user_command, shell_command, stdout, stderr,
            gemini_api_key, gemini_model_config
        )

        if status == "DONE":
            print(colorize("✅ Gemini confirms the task is complete!", Colors.OKGREEN))
            return

        if status == "CONTINUE" and next_cmd:
            print(colorize(f"💡 Gemini suggests: '{next_cmd}'", Colors.OKCYAN))
            shell_command = next_cmd
            continue

        print(colorize("⚠️ Unexpected response from Gemini; aborting.", Colors.FAIL))
        return

    print(colorize("⚠️ Reached max iterations without completion.", Colors.FAIL))


def main():
    # 1) Load API key and settings
    gemini_api_key = set_gemini_api_key()
    cmd_confirm, sec_check, gemini_cfg = read_config()
    os_name = recognize_operating_system()

    # 2) Read user’s request (speech or CLI args)
    if "--speech" in sys.argv:
        print(colorize("🎙️ Speech-to-text mode activated.", Colors.OKCYAN))
        user_cmd = audio_to_text() or ""
    else:
        user_cmd = read_user_command()

    if not user_cmd:
        print(colorize("❌ No command provided. Exiting.", Colors.FAIL))
        return

    # 3) Generate the initial shell command
    loader = LoadingDots("💡 Generating shell command")
    loader.start()
    initial_shell = generate_shell_command(user_cmd, gemini_api_key, gemini_cfg)
    loader.stop()
    print(colorize(f"📝 Initial command: {initial_shell}", Colors.OKCYAN))

    # 4) Optional safety check
    if sec_check:
        loader = LoadingDots("🔒 Checking command safety")
        loader.start()
        safe_res = is_command_safe(initial_shell, gemini_api_key, gemini_cfg)
        loader.stop()
        print(colorize(f"🔍 Safety Analysis: {safe_res}", Colors.WARNING))
        if "not safe" in safe_res.lower():
            ans = input(colorize("⚠️ Unsafe command detected. Run anyway? (yes/no): ", Colors.FAIL))
            if ans.strip().lower() != "yes":
                print(colorize("❌ Aborting on user request.", Colors.FAIL))
                return

    # 5) Enter the Gemini feedback loop
    execute_with_gemini_loop(
        user_command=user_cmd,
        initial_command=initial_shell,
        security_check=sec_check,
        gemini_api_key=gemini_api_key,
        gemini_model_config=gemini_cfg,
        command_execution_confirmation=cmd_confirm,
        operating_system=os_name
    )


if __name__ == "__main__":
    main()
