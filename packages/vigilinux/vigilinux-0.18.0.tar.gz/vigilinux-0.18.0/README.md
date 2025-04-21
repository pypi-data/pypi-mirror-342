```markdown
# Vigi - Natural Language Terminal Assistant

**Vigi** is an AI-powered terminal assistant that lets you interact with your operating system’s command-line interface using natural language. Just type what you want to do in plain English, and **Vigi** will handle the rest by generating safe, context-aware commands using Google Gemini.

---

## 🚀 Installation

Install the package directly from PyPI. The recommended way is to install it within a virtual environment or for the current user:

```bash
# Recommended (inside a virtual environment or for the current user)
pip install vigilinux

# Or specifically using pip3 if pip points to Python 2
pip3 install vigilinux
```

**Alternative (Linux System-Wide Installation - Use with Caution):**

If you need to install `vigilinux` on Linux, you can use `sudo pip3`.

```bash
# System-wide install on Linux 
sudo pip3 install vigilinux
```



---

## ⚡ Usage

Once installed, simply run `vigi` followed by your natural language command in quotes:

```bash
vigi "your natural language command here"
```

For example:

```bash
vigi "show me all Python files in the current directory"
```

**Vigi** will translate your request into the appropriate terminal command, show it to you for confirmation (unless configured otherwise), and then execute it upon approval.

---

## 🔐 API Key Setup

**First-Time Use:**
On your first run, **Vigi** will prompt you to enter your Google Gemini API key. This key is stored securely as an environment variable under the name `GEMINI_API_KEY`, so you don’t have to enter it again for subsequent uses within the same user environment setup.

**Changing the API Key:**
If you ever need to change the key, you can set the environment variable directly before running `vigi`:

*   **On Linux/macOS:**
    ```bash
    export GEMINI_API_KEY="your_new_key"
    ```
    *(To make this change permanent, add this line to your shell's configuration file, such as `~/.bashrc`, `~/.zshrc`, or `~/.profile`, and then restart your shell or run `source ~/.your_config_file`.)*

*   **On Windows (PowerShell):**
    ```powershell
    $env:GEMINI_API_KEY = "your_new_key"
    ```
    *(To make this change permanent in PowerShell, you can add this line to your PowerShell profile script. Find its location by typing `$profile` in PowerShell. Alternatively, set it permanently via the System Properties -> Environment Variables GUI.)*

*   **On Windows (Command Prompt - Temporary):**
    ```cmd
    set GEMINI_API_KEY=your_new_key
    ```
    *(This sets the variable only for the current `cmd.exe` session. For a permanent change in Command Prompt environments, use the System Properties -> Environment Variables GUI.)*

---

## 🧠 Features

*   **Natural Language Interface:** Interact with your terminal using plain English.
*   **Gemini-Powered:** Leverages Google Gemini for intelligent command generation.
*   **Context-Aware:** Remembers the current working directory for relevant commands.
*   **Cross-Platform:** Works on Linux, macOS, and Windows.
*   **Safety Focused:** Includes safeguards to prevent execution of potentially harmful commands (user confirmation is typically required).
*   **Easy Setup:** Simple installation and API key configuration.
*   **Lightweight:** Minimal dependencies.

---

## 🛠️ Requirements

*   **Python:** Version `3.6` or higher.
*   **PIP:** Python package installer.
*   **Google Gemini API Key:** A valid API key from Google AI Studio or Google Cloud.
*   **Internet Connection:** Required to communicate with the Gemini API.

---
```