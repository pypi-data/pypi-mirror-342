import os
import pandas as pd

import threading

from typing import Dict, Any, List, Optional, Union
import numpy as np
import readline
from colorama import Fore, Back, Style
import re
import tempfile
import sqlite3
import wave
import datetime
import glob
import shlex
import logging
import textwrap
import subprocess
from termcolor import colored
import sys
import termios
import tty
import pty
import select
import signal
import platform
import time

import tempfile


# Global variables
running = True
is_recording = False
recording_data = []
buffer_data = []
last_speech_time = 0


try:
    from faster_whisper import WhisperModel
    from gtts import gTTS
    import torch
    import pyaudio
    import wave
    import queue

    from npcpy.audio import (
        cleanup_temp_files,
        FORMAT,
        CHANNELS,
        RATE,
        device,
        vad_model,
        CHUNK,
        whisper_model,
        transcribe_recording,
        convert_mp3_to_wav,
    )


except Exception as e:
    print(
        "Exception: "
        + str(e)
        + "\n"
        + "Could not load the whisper package. If you want to use tts/stt features, please run `pip install npcsh[audio]` and follow the instructions in the npcsh github readme to  ensure your OS can handle the audio dependencies."
    )
try:
    from sentence_transformers import SentenceTransformer
except:

    print(
        "Could not load the sentence-transformers package. If you want to use it or other local AI features, please run `pip install npcsh[local]` ."
    )

from npcpy.load_data import (
    load_pdf,
    load_csv,
    load_json,
    load_excel,
    load_txt,
    load_image,
)
from npcpy.npc_sysenv import (
    get_model_and_provider,
    get_available_models,
    get_system_message,
    NPCSH_STREAM_OUTPUT,
    NPCSH_API_URL,
    NPCSH_CHAT_MODEL,
    NPCSH_CHAT_PROVIDER,
    NPCSH_VISION_MODEL,
    NPCSH_VISION_PROVIDER,
    NPCSH_IMAGE_GEN_MODEL,
    NPCSH_IMAGE_GEN_PROVIDER,
    NPCSH_VIDEO_GEN_MODEL,
    NPCSH_VIDEO_GEN_PROVIDER,
    print_and_process_stream
)
from npcpy.command_history import (
    CommandHistory,
    save_attachment_to_message,
    save_conversation_message,
    start_new_conversation,
)
from npcpy.embeddings import search_similar_texts, chroma_client

from npcpy.llm_funcs import (
    execute_llm_command,
    execute_llm_question,
    get_stream,
    get_conversation,
    get_llm_response,
    check_llm_command,
    generate_image,
    generate_video,
    get_embeddings,
    get_stream,
)
from npcpy.plonk import plonk, action_space
from npcpy.helpers import get_db_npcs, get_npc_path

from npcpy.npc_compiler import (
    NPC,
    Tool,
    Team,
    
)


from npcpy.search import rag_search, search_web
from npcpy.image import capture_screenshot, analyze_image

# from npcpy.audio import calibrate_silence, record_audio, speak_text
from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax
import warnings

warnings.filterwarnings("ignore", module="whisper.transcribe")

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", module="torch.serialization")
os.environ["PYTHONWARNINGS"] = "ignore"
os.environ["SDL_AUDIODRIVER"] = "dummy"

interactive_commands = {
    "ipython": ["ipython"],
    "python": ["python", "-i"],
    "sqlite3": ["sqlite3"],
    "r": ["R", "--interactive"],
}
BASH_COMMANDS = [
    "npc",
    "npm",
    "npx",
    "open",
    "alias",
    "bg",
    "bind",
    "break",
    "builtin",
    "case",
    "command",
    "compgen",
    "complete",
    "continue",
    "declare",
    "dirs",
    "disown",
    "echo",
    "enable",
    "eval",
    "exec",
    "exit",
    "export",
    "fc",
    "fg",
    "getopts",
    "hash",
    "help",
    "history",
    "if",
    "jobs",
    "kill",
    "let",
    "local",
    "logout",
    "ollama",
    "popd",
    "printf",
    "pushd",
    "pwd",
    "read",
    "readonly",
    "return",
    "set",
    "shift",
    "shopt",
    "source",
    "suspend",
    "test",
    "times",
    "trap",
    "type",
    "typeset",
    "ulimit",
    "umask",
    "unalias",
    "unset",
    "until",
    "wait",
    "while",
    # Common Unix commands
    "ls",
    "cp",
    "mv",
    "rm",
    "mkdir",
    "rmdir",
    "touch",
    "cat",
    "less",
    "more",
    "head",
    "tail",
    "grep",
    "find",
    "sed",
    "awk",
    "sort",
    "uniq",
    "wc",
    "diff",
    "chmod",
    "chown",
    "chgrp",
    "ln",
    "tar",
    "gzip",
    "gunzip",
    "zip",
    "unzip",
    "ssh",
    "scp",
    "rsync",
    "wget",
    "curl",
    "ping",
    "netstat",
    "ifconfig",
    "route",
    "traceroute",
    "ps",
    "top",
    "htop",
    "kill",
    "killall",
    "su",
    "sudo",
    "whoami",
    "who",
    "w",
    "last",
    "finger",
    "uptime",
    "free",
    "df",
    "du",
    "mount",
    "umount",
    "fdisk",
    "mkfs",
    "fsck",
    "dd",
    "cron",
    "at",
    "systemctl",
    "service",
    "journalctl",
    "man",
    "info",
    "whatis",
    "whereis",
    "which",
    "date",
    "cal",
    "bc",
    "expr",
    "screen",
    "tmux",
    "git",
    "vim",
    "emacs",
    "nano",
    "pip",
]


def preprocess_code_block(code_text):
    """
    Preprocess code block text to remove leading spaces.
    """
    lines = code_text.split("\n")
    return "\n".join(line.lstrip() for line in lines)


def preprocess_markdown(md_text):
    """
    Preprocess markdown text to handle code blocks separately.
    """
    lines = md_text.split("\n")
    processed_lines = []

    inside_code_block = False
    current_code_block = []

    for line in lines:
        if line.startswith("```"):  # Toggle code block
            if inside_code_block:
                # Close code block, unindent, and append
                processed_lines.append("```")
                processed_lines.extend(
                    textwrap.dedent("\n".join(current_code_block)).split("\n")
                )
                processed_lines.append("```")
                current_code_block = []
            inside_code_block = not inside_code_block
        elif inside_code_block:
            current_code_block.append(line)
        else:
            processed_lines.append(line)

    return "\n".join(processed_lines)


def render_markdown(text: str) -> None:
    """
    Renders markdown text, but handles code blocks as plain syntax-highlighted text.
    """
    lines = text.split("\n")
    console = Console()

    inside_code_block = False
    code_lines = []
    lang = None

    for line in lines:
        if line.startswith("```"):
            if inside_code_block:
                # End of code block - render the collected code
                code = "\n".join(code_lines)
                if code.strip():
                    syntax = Syntax(
                        code, lang or "python", theme="monokai", line_numbers=False
                    )
                    console.print(syntax)
                code_lines = []
            else:
                # Start of code block - get language if specified
                lang = line[3:].strip() or None
            inside_code_block = not inside_code_block
        elif inside_code_block:
            code_lines.append(line)
        else:
            # Regular markdown
            console.print(Markdown(line))


def change_directory(command_parts: list, messages: list) -> dict:
    """
    Function Description:
        Changes the current directory.
    Args:
        command_parts : list : Command parts
        messages : list : Messages
    Keyword Args:
        None
    Returns:
        dict : dict : Dictionary

    """

    try:
        if len(command_parts) > 1:
            new_dir = os.path.expanduser(command_parts[1])
        else:
            new_dir = os.path.expanduser("~")
        os.chdir(new_dir)
        return {
            "messages": messages,
            "output": f"Changed directory to {os.getcwd()}",
        }
    except FileNotFoundError:
        return {
            "messages": messages,
            "output": f"Directory not found: {new_dir}",
        }
    except PermissionError:
        return {"messages": messages, "output": f"Permission denied: {new_dir}"}


def log_action(action: str, detail: str = "") -> None:
    """
    Function Description:
        This function logs an action with optional detail.
    Args:
        action: The action to log.
        detail: Additional detail to log.
    Keyword Args:
        None
    Returns:
        None
    """
    logging.info(f"{action}: {detail}")


TERMINAL_EDITORS = ["vim", "emacs", "nano"]


def complete(text: str, state: int) -> str:
    """
    Function Description:
        Handles autocompletion for the npcsh shell.
    Args:
        text : str : Text to autocomplete
        state : int : State
    Keyword Args:
        None
    Returns:
        None

    """
    buffer = readline.get_line_buffer()
    available_chat_models, available_reasoning_models = get_available_models()
    available_models = available_chat_models + available_reasoning_models

    # If completing a model name
    if "@" in buffer:
        at_index = buffer.rfind("@")
        model_text = buffer[at_index + 1 :]
        model_completions = [m for m in available_models if m.startswith(model_text)]

        try:
            # Return the full text including @ symbol
            return "@" + model_completions[state]
        except IndexError:
            return None

    # If completing a command
    elif text.startswith("/"):
        command_completions = [c for c in valid_commands if c.startswith(text)]
        try:
            return command_completions[state]
        except IndexError:
            return None

    return None


def global_completions(text: str, command_parts: list) -> list:
    """
    Function Description:
        Handles global autocompletions for the npcsh shell.
    Args:
        text : str : Text to autocomplete
        command_parts : list : List of command parts
    Keyword Args:
        None
    Returns:
        completions : list : List of completions

    """
    if not command_parts:
        return [c + " " for c in valid_commands if c.startswith(text)]
    elif command_parts[0] in ["/compile", "/com"]:
        # Autocomplete NPC files
        return [f for f in os.listdir(".") if f.endswith(".npc") and f.startswith(text)]
    elif command_parts[0] == "/read":
        # Autocomplete filenames
        return [f for f in os.listdir(".") if f.startswith(text)]
    else:
        # Default filename completion
        return [f for f in os.listdir(".") if f.startswith(text)]


def wrap_text(text: str, width: int = 80) -> str:
    """
    Function Description:
        Wraps text to a specified width.
    Args:
        text : str : Text to wrap
        width : int : Width of text
    Keyword Args:
        None
    Returns:
        lines : str : Wrapped text
    """
    lines = []
    for paragraph in text.split("\n"):
        lines.extend(textwrap.wrap(paragraph, width=width))
    return "\n".join(lines)


def get_file_color(filepath: str) -> tuple:
    """
    Function Description:
        Returns color and attributes for a given file path.
    Args:
        filepath : str : File path
    Keyword Args:
        None
    Returns:
        color : str : Color
        attrs : list : List of attributes

    """

    if os.path.isdir(filepath):
        return "blue", ["bold"]
    elif os.access(filepath, os.X_OK):
        return "green", []
    elif filepath.endswith((".zip", ".tar", ".gz", ".bz2", ".xz", ".7z")):
        return "red", []
    elif filepath.endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff")):
        return "magenta", []
    elif filepath.endswith((".py", ".pyw")):
        return "yellow", []
    elif filepath.endswith((".sh", ".bash", ".zsh")):
        return "green", []
    elif filepath.endswith((".c", ".cpp", ".h", ".hpp")):
        return "cyan", []
    elif filepath.endswith((".js", ".ts", ".jsx", ".tsx")):
        return "yellow", []
    elif filepath.endswith((".html", ".css", ".scss", ".sass")):
        return "magenta", []
    elif filepath.endswith((".md", ".txt", ".log")):
        return "white", []
    elif filepath.startswith("."):
        return "cyan", []
    else:
        return "white", []


def readline_safe_prompt(prompt: str) -> str:
    """
    Function Description:
        Escapes ANSI escape sequences in the prompt.
    Args:
        prompt : str : Prompt
    Keyword Args:
        None
    Returns:
        prompt : str : Prompt

    """
    # This regex matches ANSI escape sequences
    ansi_escape = re.compile(r"(\033\[[0-9;]*[a-zA-Z])")

    # Wrap them with \001 and \002
    def escape_sequence(m):
        return "\001" + m.group(1) + "\002"

    return ansi_escape.sub(escape_sequence, prompt)


def setup_readline() -> str:
    """
    Function Description:
        Sets up readline for the npcsh shell.
    Args:
        None
    Keyword Args:
        None
    Returns:
        history_file : str : History file
    """
    history_file = os.path.expanduser("~/.npcsh_history")
    try:
        readline.read_history_file(history_file)
    except FileNotFoundError:
        pass

    readline.set_history_length(1000)
    readline.parse_and_bind("set enable-bracketed-paste on")  # Enable paste mode
    readline.parse_and_bind(r'"\e[A": history-search-backward')
    readline.parse_and_bind(r'"\e[B": history-search-forward')
    readline.parse_and_bind(r'"\C-r": reverse-search-history')
    readline.parse_and_bind(r'\C-e: end-of-line')
    readline.parse_and_bind(r'\C-a: beginning-of-line')

    return history_file


def save_readline_history():
    readline.write_history_file(os.path.expanduser("~/.npcsh_readline_history"))


def orange(text: str) -> str:
    """
    Function Description:
        Returns orange text.
    Args:
        text : str : Text
    Keyword Args:
        None
    Returns:
        text : str : Text

    """
    return f"\033[38;2;255;165;0m{text}{Style.RESET_ALL}"


def get_multiline_input(prompt: str) -> str:
    """
    Function Description:
        Gets multiline input from the user.
    Args:
        prompt : str : Prompt
    Keyword Args:
        None
    Returns:
        lines : str : Lines

    """
    lines = []
    current_prompt = prompt
    while True:
        try:
            line = input(current_prompt)
        except EOFError:
            print("Goodbye!")
            break

        if line.endswith("\\"):
            lines.append(line[:-1])  # Remove the backslash
            # Use a continuation prompt for the next line
            current_prompt = readline_safe_prompt("> ")
        else:
            lines.append(line)
            break

    return "\n".join(lines)


def start_interactive_session(command: list) -> int:
    """
    Function Description:
        Starts an interactive session.
    Args:
        command : list : Command to execute
    Keyword Args:
        None
    Returns:
        returncode : int : Return code

    """
    # Save the current terminal settings
    old_tty = termios.tcgetattr(sys.stdin)
    try:
        # Create a pseudo-terminal
        master_fd, slave_fd = pty.openpty()

        # Start the process
        p = subprocess.Popen(
            command,
            stdin=slave_fd,
            stdout=slave_fd,
            stderr=slave_fd,
            shell=True,
            preexec_fn=os.setsid,  # Create a new process group
        )

        # Set the terminal to raw mode
        tty.setraw(sys.stdin.fileno())

        def handle_timeout(signum, frame):
            raise TimeoutError("Process did not terminate in time")

        while p.poll() is None:
            r, w, e = select.select([sys.stdin, master_fd], [], [], 0.1)
            if sys.stdin in r:
                d = os.read(sys.stdin.fileno(), 10240)
                os.write(master_fd, d)
            elif master_fd in r:
                o = os.read(master_fd, 10240)
                if o:
                    os.write(sys.stdout.fileno(), o)
                else:
                    break

        # Wait for the process to terminate with a timeout
        signal.signal(signal.SIGALRM, handle_timeout)
        signal.alarm(5)  # 5 second timeout
        try:
            p.wait()
        except TimeoutError:
            print("\nProcess did not terminate. Force killing...")
            os.killpg(os.getpgid(p.pid), signal.SIGTERM)
            time.sleep(1)
            if p.poll() is None:
                os.killpg(os.getpgid(p.pid), signal.SIGKILL)
        finally:
            signal.alarm(0)

    finally:
        # Restore the terminal settings
        termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, old_tty)

    return p.returncode


def validate_bash_command(command_parts: list) -> bool:
    """
    Function Description:
        Validate if the command sequence is a valid bash command with proper arguments/flags.
    Args:
        command_parts : list : Command parts
    Keyword Args:
        None
    Returns:
        bool : bool : Boolean
    """
    if not command_parts:
        return False

    COMMAND_PATTERNS = {
        "cat": {
            "flags": ["-n", "-b", "-E", "-T", "-s", "--number", "-A", "--show-all"],
            "requires_arg": True,
        },
        "find": {
            "flags": [
                "-name",
                "-type",
                "-size",
                "-mtime",
                "-exec",
                "-print",
                "-delete",
                "-maxdepth",
                "-mindepth",
                "-perm",
                "-user",
                "-group",
            ],
            "requires_arg": True,
        },
        "who": {
            "flags": [
                "-a",
                "-b",
                "-d",
                "-H",
                "-l",
                "-p",
                "-q",
                "-r",
                "-s",
                "-t",
                "-u",
                "--all",
                "--count",
                "--heading",
            ],
            "requires_arg": True,
        },
        "open": {
            "flags": ["-a", "-e", "-t", "-f", "-F", "-W", "-n", "-g", "-h"],
            "requires_arg": True,
        },
        "which": {"flags": ["-a", "-s", "-v"], "requires_arg": True},
    }

    base_command = command_parts[0]

    if base_command not in COMMAND_PATTERNS:
        return True  # Allow other commands to pass through

    pattern = COMMAND_PATTERNS[base_command]
    args = []
    flags = []

    for i in range(1, len(command_parts)):
        part = command_parts[i]
        if part.startswith("-"):
            flags.append(part)
            if part not in pattern["flags"]:
                return False  # Invalid flag
        else:
            args.append(part)

    # Check if 'who' has any arguments (it shouldn't)
    if base_command == "who" and args:
        return False

    # Handle 'which' with '-a' flag
    if base_command == "which" and "-a" in flags:
        return True  # Allow 'which -a' with or without arguments.

    # Check if any required arguments are missing
    if pattern.get("requires_arg", False) and not args:
        return False

    return True


def execute_squish_command():
    return


def execute_splat_command():
    return


def execute_rag_command(
    command: str,
    messages=None,
) -> dict:
    """
    Execute the RAG command with support for embedding generation using
    nomic-embed-text.
    """

    if messages is None:
        messages = []

    parts = command.split()
    search_terms = []
    params = {}
    file_list = []

    # Parse command parts
    for i, part in enumerate(parts):
        if "=" in part:  # This is a parameter
            key, value = part.split("=", 1)
            params[key.strip()] = value.strip()
        elif part.startswith("-f"):  # Handle the file list
            if i + 1 < len(parts):
                wildcard_pattern = parts[i + 1]
                file_list.extend(glob.glob(wildcard_pattern))
        else:  # This is part of the search term
            search_terms.append(part)

    # print(params)
    # -top_k  will also be a flaggable param
    if "-top_k" in params:
        top_k = int(params["-top_k"])
    else:
        top_k = 5

    # If no files found, inform the user
    if not file_list:
        return {
            "messages": messages,
            "output": "No files found matching the specified pattern.",
        }

    search_term = " ".join(search_terms)
    docs_to_embed = []

    # try:
    # Load each file and generate embeddings
    for filename in file_list:
        extension = os.path.splitext(filename)[1].lower()
        if os.path.exists(filename):
            if extension in [
                ".txt",
                ".csv",
                ".yaml",
                ".json",
                ".md",
                ".r",
                ".c",
                ".java",
                ".cpp",
                ".h",
                ".hpp",
                ".xlsx",
                ".py",
                ".js",
                ".ts",
                ".html",
                ".css",
                ".ipynb",
                ".pdf",
                ".docx",
                ".pptx",
                ".ppt",
                ".npc",
                ".tool",
                ".doc",
                ".xls",
            ]:
                if extension == ".csv":
                    df = pd.read_csv(filename)
                    file_texts = df.apply(
                        lambda row: " ".join(row.values.astype(str)), axis=1
                    ).tolist()
                else:
                    with open(filename, "r", encoding="utf-8") as file:
                        file_texts = file.readlines()
                    file_texts = [
                        line.strip() for line in file_texts if line.strip() != ""
                    ]
                    docs_to_embed.extend(file_texts)
            else:
                return {
                    "messages": messages,
                    "output": f"Unsupported file type: {extension} for file {filename}",
                }

    similar_texts = search_similar_texts(
        search_term,
        docs_to_embed=docs_to_embed,
        top_k=top_k,  # Adjust as necessary
    )

    # Format results
    output = "Found similar texts:\n\n"
    if similar_texts:
        for result in similar_texts:
            output += f"Score: {result['score']:.3f}\n"
            output += f"Text: {result['text']}\n"
            if "id" in result:
                output += f"ID: {result['id']}\n"
            output += "\n"
    else:
        output = "No similar texts found in the database."

    # Additional information about processed files
    output += "\nProcessed Files:\n"
    output += "\n".join(file_list)

    return {"messages": messages, "output": output}

    # except Exception as e:
    #    return {
    #        "messages": messages,
    #        "output": f"Error during RAG search: {str(e)}",
    #    }


def filter_by_date(
    similar_texts: List[dict], start_date: str, end_date: str
) -> List[dict]:
    """
    Filter the similar texts based on start and end dates.
    Args:
        similar_texts (List[dict]): The similar texts to filter.
        start_date (str): The start date in 'YYYY-MM-DD' format.
        end_date (str): The end date in 'YYYY-MM-DD' format.

    Returns:
        List[dict]: Filtered similar texts.
    """
    filtered_results = []
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    for text in similar_texts:
        text_date = datetime.strptime(
            text["date"], "%Y-%m-%d"
        )  # Assuming 'date' is an attribut

        if start <= text_date <= end:
            filtered_results.append(text)

    return filtered_results


def execute_search_command(
    command: str,
    messages=None,
    provider: str = None,
):
    """
    Function Description:
        Executes a search command.
    Args:
        command : str : Command
        db_path : str : Database path

    Keyword Args:
        embedding_model : None : Embedding model
        current_npc : None : Current NPC
        text_data : None : Text data
        text_data_embedded : None : Embedded text data
        messages : None : Messages
    Returns:
        dict : dict : Dictionary

    """
    # search commands will bel ike :
    # '/search -p default = google "search term" '
    # '/search -p perplexity ..
    # '/search -p google ..
    # extract provider if its there
    # check for either -p or --p

    search_command = command.split()
    if any("-p" in s for s in search_command) or any(
        "--provider" in s for s in search_command
    ):
        provider = (
            search_command[search_command.index("-p") + 1]
            if "-p" in search_command
            else search_command[search_command.index("--provider") + 1]
        )
    else:
        provider = None
    if any("-n" in s for s in search_command) or any(
        "--num_results" in s for s in search_command
    ):
        num_results = (
            search_command[search_command.index("-n") + 1]
            if "-n" in search_command
            else search_command[search_command.index("--num_results") + 1]
        )
    else:
        num_results = 5

    # remove the -p and provider from the command string
    command = command.replace(f"-p {provider}", "").replace(
        f"--provider {provider}", ""
    )
    result = search_web(command, num_results=num_results, provider=provider)
    if messages is None:
        messages = []
        messages.append({"role": "user", "content": command})

    messages.append(
        {"role": "assistant", "content": result[0] + f" \n Citation Links: {result[1]}"}
    )

    return {
        "messages": messages,
        "output": result[0] + f"\n\n\n Citation Links: {result[1]}",
    }


def extract_tool_inputs(args: List[str], tool: Tool) -> Dict[str, Any]:
    inputs = {}

    # Create flag mapping
    flag_mapping = {}
    for input_ in tool.inputs:
        if isinstance(input_, str):
            flag_mapping[f"-{input_[0]}"] = input_
            flag_mapping[f"--{input_}"] = input_
        elif isinstance(input_, dict):
            key = list(input_.keys())[0]
            flag_mapping[f"-{key[0]}"] = key
            flag_mapping[f"--{key}"] = key

    # Process arguments
    used_args = set()
    for i, arg in enumerate(args):
        if arg in flag_mapping:
            # If flag is found, next argument is its value
            if i + 1 < len(args):
                input_name = flag_mapping[arg]
                inputs[input_name] = args[i + 1]
                used_args.add(i)
                used_args.add(i + 1)
            else:
                print(f"Warning: {arg} flag is missing a value.")

    # If no flags used, combine remaining args for first input
    unused_args = [arg for i, arg in enumerate(args) if i not in used_args]
    if unused_args and tool.inputs:
        first_input = tool.inputs[0]
        if isinstance(first_input, str):
            inputs[first_input] = " ".join(unused_args)
        elif isinstance(first_input, dict):
            key = list(first_input.keys())[0]
            inputs[key] = " ".join(unused_args)

    # Add default values for inputs not provided
    for input_ in tool.inputs:
        if isinstance(input_, str):
            if input_ not in inputs:
                if any(args):  # If we have any arguments at all
                    raise ValueError(f"Missing required input: {input_}")
                else:
                    inputs[input_] = None  # Allow None for completely empty calls
        elif isinstance(input_, dict):
            key = list(input_.keys())[0]
            if key not in inputs:
                inputs[key] = input_[key]

    return inputs


import math
from PIL import Image


def resize_image_tars(image_path):
    image = Image.open(image_path)
    max_pixels = 6000 * 28 * 28
    if image.width * image.height > max_pixels:
        max_pixels = 2700 * 28 * 28
    else:
        max_pixels = 1340 * 28 * 28
    resize_factor = math.sqrt(max_pixels / (image.width * image.height))
    width, height = int(image.width * resize_factor), int(image.height * resize_factor)
    image = image.resize((width, height))
    image.save(image_path, format="png")


def execute_plan_command(
    command, npc=None, model=None, provider=None, messages=None, api_url=None
):
    parts = command.split(maxsplit=1)
    if len(parts) < 2:
        return {
            "messages": messages,
            "output": "Usage: /plan <command and schedule description>",
        }

    request = parts[1]
    platform_system = platform.system()

    # Create standard directories
    jobs_dir = os.path.expanduser("~/.npcsh/jobs")
    logs_dir = os.path.expanduser("~/.npcsh/logs")
    os.makedirs(jobs_dir, exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)

    # First part - just the request formatting
    linux_request = f"""Convert this scheduling request into a crontab-based script:
    Request: {request}

    """

    # Second part - the static prompt with examples and requirements
    linux_prompt_static = """Example for "record CPU usage every 10 minutes":
    {
        "script": "#!/bin/bash
set -euo pipefail
IFS=$'\\n\\t'

LOGFILE=\"$HOME/.npcsh/logs/cpu_usage.log\"

log_info() {
    echo \"[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] $*\" >> \"$LOGFILE\"
}

log_error() {
    echo \"[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR] $*\" >> \"$LOGFILE\"
}

record_cpu() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local cpu_usage=$(top -bn1 | grep 'Cpu(s)' | awk '{print $2}')
    log_info \"CPU Usage: $cpu_usage%\"
}

record_cpu",
        "schedule": "*/10 * * * *",
        "description": "Record CPU usage every 10 minutes",
        "name": "record_cpu_usage"
    }

    Your response must be valid json with the following keys:
    - script: The shell script content with proper functions and error handling. special characters must be escaped to ensure python json.loads will work correctly.
    - schedule: Crontab expression (5 fields: minute hour day month weekday)
    - description: A human readable description
    - name: A unique name for the job

    Do not include any additional markdown formatting in your response or leading ```json tags."""

    mac_request = f"""Convert this scheduling request into a launchd-compatible script:
    Request: {request}

    """

    mac_prompt_static = """Example for "record CPU usage every 10 minutes":
    {
        "script": "#!/bin/bash
set -euo pipefail
IFS=$'\\n\\t'

LOGFILE=\"$HOME/.npcsh/logs/cpu_usage.log\"

log_info() {
    echo \"[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] $*\" >> \"$LOGFILE\"
}

log_error() {
    echo \"[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR] $*\" >> \"$LOGFILE\"
}

record_cpu() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local cpu_usage=$(top -l 1 | grep 'CPU usage' | awk '{print $3}' | tr -d '%')
    log_info \"CPU Usage: $cpu_usage%\"
}

record_cpu",
        "schedule": "600",
        "description": "Record CPU usage every 10 minutes",
        "name": "record_cpu_usage"
    }

    Your response must be valid json with the following keys:
    - script: The shell script content with proper functions and error handling. special characters must be escaped to ensure python json.loads will work correctly.
    - schedule: Interval in seconds (e.g. 600 for 10 minutes)
    - description: A human readable description
    - name: A unique name for the job

    Do not include any additional markdown formatting in your response or leading ```json tags."""

    windows_request = f"""Convert this scheduling request into a PowerShell script with Task Scheduler parameters:
    Request: {request}

    """

    windows_prompt_static = """Example for "record CPU usage every 10 minutes":
    {
        "script": "$ErrorActionPreference = 'Stop'

$LogFile = \"$HOME\\.npcsh\\logs\\cpu_usage.log\"

function Write-Log {
    param($Message, $Type = 'INFO')
    $timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    \"[$timestamp] [$Type] $Message\" | Out-File -FilePath $LogFile -Append
}

function Get-CpuUsage {
    try {
        $cpu = (Get-Counter '\\Processor(_Total)\\% Processor Time').CounterSamples.CookedValue
        Write-Log \"CPU Usage: $($cpu)%\"
    } catch {
        Write-Log $_.Exception.Message 'ERROR'
        throw
    }
}

Get-CpuUsage",
        "schedule": "/sc minute /mo 10",
        "description": "Record CPU usage every 10 minutes",
        "name": "record_cpu_usage"
    }

    Your response must be valid json with the following keys:
    - script: The PowerShell script content with proper functions and error handling. special characters must be escaped to ensure python json.loads will work correctly.
    - schedule: Task Scheduler parameters (e.g. /sc minute /mo 10)
    - description: A human readable description
    - name: A unique name for the job

    Do not include any additional markdown formatting in your response or leading ```json tags."""

    prompts = {
        "Linux": linux_request + linux_prompt_static,
        "Darwin": mac_request + mac_prompt_static,
        "Windows": windows_request + windows_prompt_static,
    }

    prompt = prompts[platform_system]
    response = get_llm_response(
        prompt, npc=npc, model=model, provider=provider, format="json"
    )
    schedule_info = response.get("response")
    print("Received schedule info:", schedule_info)

    job_name = f"job_{schedule_info['name']}"

    if platform_system == "Windows":
        script_path = os.path.join(jobs_dir, f"{job_name}.ps1")
    else:
        script_path = os.path.join(jobs_dir, f"{job_name}.sh")

    log_path = os.path.join(logs_dir, f"{job_name}.log")

    # Write the script
    with open(script_path, "w") as f:
        f.write(schedule_info["script"])
    os.chmod(script_path, 0o755)

    if platform_system == "Linux":
        try:
            current_crontab = subprocess.check_output(["crontab", "-l"], text=True)
        except subprocess.CalledProcessError:
            current_crontab = ""

        crontab_line = f"{schedule_info['schedule']} {script_path} >> {log_path} 2>&1"
        new_crontab = current_crontab.strip() + "\n" + crontab_line + "\n"

        with tempfile.NamedTemporaryFile(mode="w") as tmp:
            tmp.write(new_crontab)
            tmp.flush()
            subprocess.run(["crontab", tmp.name], check=True)

        output = f"""Job created successfully:
- Description: {schedule_info['description']}
- Schedule: {schedule_info['schedule']}
- Script: {script_path}
- Log: {log_path}
- Crontab entry: {crontab_line}"""

    elif platform_system == "Darwin":
        plist_dir = os.path.expanduser("~/Library/LaunchAgents")
        os.makedirs(plist_dir, exist_ok=True)
        plist_path = os.path.join(plist_dir, f"com.npcsh.{job_name}.plist")

        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.npcsh.{job_name}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{script_path}</string>
    </array>
    <key>StartInterval</key>
    <integer>{schedule_info['schedule']}</integer>
    <key>StandardOutPath</key>
    <string>{log_path}</string>
    <key>StandardErrorPath</key>
    <string>{log_path}</string>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>"""

        with open(plist_path, "w") as f:
            f.write(plist_content)

        subprocess.run(["launchctl", "unload", plist_path], check=False)
        subprocess.run(["launchctl", "load", plist_path], check=True)

        output = f"""Job created successfully:
- Description: {schedule_info['description']}
- Schedule: Every {schedule_info['schedule']} seconds
- Script: {script_path}
- Log: {log_path}
- Launchd plist: {plist_path}"""

    elif platform_system == "Windows":
        task_name = f"NPCSH_{job_name}"

        # Parse schedule_info['schedule'] into individual parameters
        schedule_params = schedule_info["schedule"].split()

        cmd = (
            [
                "schtasks",
                "/create",
                "/tn",
                task_name,
                "/tr",
                f"powershell -NoProfile -ExecutionPolicy Bypass -File {script_path}",
            ]
            + schedule_params
            + ["/f"]
        )  # /f forces creation if task exists

        subprocess.run(cmd, check=True)

        output = f"""Job created successfully:
- Description: {schedule_info['description']}
- Schedule: {schedule_info['schedule']}
- Script: {script_path}
- Log: {log_path}
- Task name: {task_name}"""

    return {"messages": messages, "output": output}


def execute_trigger_command(
    command, npc=None, model=None, provider=None, messages=None, api_url=None
):
    parts = command.split(maxsplit=1)
    if len(parts) < 2:
        return {
            "messages": messages,
            "output": "Usage: /trigger <trigger condition and action description>",
        }

    request = parts[1]
    platform_system = platform.system()

    linux_request = f"""Convert this trigger request into a single event-monitoring daemon script:
    Request: {request}

    """

    linux_prompt_static = """Example for "Move PDFs from Downloads to Documents/PDFs":
    {
        "script": "#!/bin/bash\\nset -euo pipefail\\nIFS=$'\\n\\t'\\n\\nLOGFILE=\\\"$HOME/.npcsh/logs/pdf_mover.log\\\"\\nSOURCE=\\\"$HOME/Downloads\\\"\\nTARGET=\\\"$HOME/Documents/PDFs\\\"\\n\\nlog_info() {\\n    echo \\\"[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] $*\\\" >> \\\"$LOGFILE\\\"\\n}\\n\\nlog_error() {\\n    echo \\\"[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR] $*\\\" >> \\\"$LOGFILE\\\"\\n}\\n\\ninotifywait -m -q -e create --format '%w%f' \\\"$SOURCE\\\" | while read filepath; do\\n    if [[ \\\"$filepath\\\" =~ \\\\.pdf$ ]]; then\\n        mv \\\"$filepath\\\" \\\"$TARGET/\\\" && log_info \\\"Moved $filepath to $TARGET\\\" || log_error \\\"Failed to move $filepath\\\"\\n    fi\\ndone",
        "name": "pdf_mover",
        "description": "Move PDF files from Downloads to Documents/PDFs folder"
    }

    The script MUST:
    - Use inotifywait -m -q -e create --format '%w%f' to get full paths
    - Double quote ALL file operations: "$SOURCE/$FILE"
    - Use $HOME for absolute paths
    - Echo both success and failure messages to log

    Your response must be valid json with the following keys:
    - script: The shell script content with proper functions and error handling
    - name: A unique name for the trigger
    - description: A human readable description

    Do not include any additional markdown formatting in your response."""

    mac_request = f"""Convert this trigger request into a single event-monitoring daemon script:
    Request: {request}

    """

    mac_prompt_static = """Example for "Move PDFs from Downloads to Documents/PDFs":
    {
        "script": "#!/bin/bash\\nset -euo pipefail\\nIFS=$'\\n\\t'\\n\\nLOGFILE=\\\"$HOME/.npcsh/logs/pdf_mover.log\\\"\\nSOURCE=\\\"$HOME/Downloads\\\"\\nTARGET=\\\"$HOME/Documents/PDFs\\\"\\n\\nlog_info() {\\n    echo \\\"[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] $*\\\" >> \\\"$LOGFILE\\\"\\n}\\n\\nlog_error() {\\n    echo \\\"[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR] $*\\\" >> \\\"$LOGFILE\\\"\\n}\\n\\nfswatch -0 -r -e '.*' --event Created --format '%p' \\\"$SOURCE\\\" | while read -d '' filepath; do\\n    if [[ \\\"$filepath\\\" =~ \\\\.pdf$ ]]; then\\n        mv \\\"$filepath\\\" \\\"$TARGET/\\\" && log_info \\\"Moved $filepath to $TARGET\\\" || log_error \\\"Failed to move $filepath\\\"\\n    fi\\ndone",
        "name": "pdf_mover",
        "description": "Move PDF files from Downloads to Documents/PDFs folder"
    }

    The script MUST:
    - Use fswatch -0 -r -e '.*' --event Created --format '%p' to get full paths
    - Double quote ALL file operations: "$SOURCE/$FILE"
    - Use $HOME for absolute paths
    - Echo both success and failure messages to log

    Your response must be valid json with the following keys:
    - script: The shell script content with proper functions and error handling
    - name: A unique name for the trigger
    - description: A human readable description

    Do not include any additional markdown formatting in your response."""

    windows_request = f"""Convert this trigger request into a single event-monitoring daemon script:
    Request: {request}

    """

    windows_prompt_static = """Example for "Move PDFs from Downloads to Documents/PDFs":
    {
        "script": "$ErrorActionPreference = 'Stop'\\n\\n$LogFile = \\\"$HOME\\.npcsh\\logs\\pdf_mover.log\\\"\\n$Source = \\\"$HOME\\Downloads\\\"\\n$Target = \\\"$HOME\\Documents\\PDFs\\\"\\n\\nfunction Write-Log {\\n    param($Message, $Type = 'INFO')\\n    $timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'\\n    \\\"[$timestamp] [$Type] $Message\\\" | Out-File -FilePath $LogFile -Append\\n}\\n\\n$watcher = New-Object System.IO.FileSystemWatcher\\n$watcher.Path = $Source\\n$watcher.Filter = \\\"*.pdf\\\"\\n$watcher.IncludeSubdirectories = $true\\n$watcher.EnableRaisingEvents = $true\\n\\n$action = {\\n    $path = $Event.SourceEventArgs.FullPath\\n    try {\\n        Move-Item -Path $path -Destination $Target\\n        Write-Log \\\"Moved $path to $Target\\\"\\n    } catch {\\n        Write-Log $_.Exception.Message 'ERROR'\\n    }\\n}\\n\\nRegister-ObjectEvent $watcher 'Created' -Action $action\\n\\nwhile ($true) { Start-Sleep 1 }",
        "name": "pdf_mover",
        "description": "Move PDF files from Downloads to Documents/PDFs folder"
    }

    The script MUST:
    - Use FileSystemWatcher for monitoring
    - Double quote ALL file operations: "$Source\\$File"
    - Use $HOME for absolute paths
    - Echo both success and failure messages to log

    Your response must be valid json with the following keys:
    - script: The PowerShell script content with proper functions and error handling
    - name: A unique name for the trigger
    - description: A human readable description

    Do not include any additional markdown formatting in your response."""

    prompts = {
        "Linux": linux_request + linux_prompt_static,
        "Darwin": mac_request + mac_prompt_static,
        "Windows": windows_request + windows_prompt_static,
    }

    prompt = prompts[platform_system]
    response = get_llm_response(
        prompt, npc=npc, model=model, provider=provider, format="json"
    )
    trigger_info = response.get("response")
    print("Trigger info:", trigger_info)

    triggers_dir = os.path.expanduser("~/.npcsh/triggers")
    logs_dir = os.path.expanduser("~/.npcsh/logs")
    os.makedirs(triggers_dir, exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)

    trigger_name = f"trigger_{trigger_info['name']}"
    log_path = os.path.join(logs_dir, f"{trigger_name}.log")

    if platform_system == "Linux":
        script_path = os.path.join(triggers_dir, f"{trigger_name}.sh")

        with open(script_path, "w") as f:
            f.write(trigger_info["script"])
        os.chmod(script_path, 0o755)

        service_dir = os.path.expanduser("~/.config/systemd/user")
        os.makedirs(service_dir, exist_ok=True)
        service_path = os.path.join(service_dir, f"npcsh-{trigger_name}.service")

        service_content = f"""[Unit]
Description={trigger_info['description']}
After=network.target

[Service]
Type=simple
ExecStart={script_path}
Restart=always
StandardOutput=append:{log_path}
StandardError=append:{log_path}

[Install]
WantedBy=default.target
"""

        with open(service_path, "w") as f:
            f.write(service_content)

        subprocess.run(["systemctl", "--user", "daemon-reload"])
        subprocess.run(
            ["systemctl", "--user", "enable", f"npcsh-{trigger_name}.service"]
        )
        subprocess.run(
            ["systemctl", "--user", "start", f"npcsh-{trigger_name}.service"]
        )

        status = subprocess.run(
            ["systemctl", "--user", "status", f"npcsh-{trigger_name}.service"],
            capture_output=True,
            text=True,
        )

        output = f"""Trigger service created:
- Description: {trigger_info['description']}
- Script: {script_path}
- Service: {service_path}
- Log: {log_path}

Status:
{status.stdout}"""

    elif platform_system == "Darwin":
        script_path = os.path.join(triggers_dir, f"{trigger_name}.sh")

        with open(script_path, "w") as f:
            f.write(trigger_info["script"])
        os.chmod(script_path, 0o755)

        plist_dir = os.path.expanduser("~/Library/LaunchAgents")
        os.makedirs(plist_dir, exist_ok=True)
        plist_path = os.path.join(plist_dir, f"com.npcsh.{trigger_name}.plist")

        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.npcsh.{trigger_name}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{script_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>{log_path}</string>
    <key>StandardErrorPath</key>
    <string>{log_path}</string>
</dict>
</plist>"""

        with open(plist_path, "w") as f:
            f.write(plist_content)

        subprocess.run(["launchctl", "unload", plist_path], check=False)
        subprocess.run(["launchctl", "load", plist_path], check=True)

        output = f"""Trigger service created:
- Description: {trigger_info['description']}
- Script: {script_path}
- Launchd plist: {plist_path}
- Log: {log_path}"""

    elif platform_system == "Windows":
        script_path = os.path.join(triggers_dir, f"{trigger_name}.ps1")

        with open(script_path, "w") as f:
            f.write(trigger_info["script"])

        task_name = f"NPCSH_{trigger_name}"

        # Create a scheduled task that runs at startup
        cmd = [
            "schtasks",
            "/create",
            "/tn",
            task_name,
            "/tr",
            f"powershell -NoProfile -ExecutionPolicy Bypass -File {script_path}",
            "/sc",
            "onstart",
            "/ru",
            "System",
            "/f",  # Force creation
        ]

        subprocess.run(cmd, check=True)

        # Start the task immediately
        subprocess.run(["schtasks", "/run", "/tn", task_name])

        output = f"""Trigger service created:
- Description: {trigger_info['description']}
- Script: {script_path}
- Task name: {task_name}
- Log: {log_path}"""

    return {"messages": messages, "output": output}


def enter_wander_mode(args, messages, npc_compiler, npc, model, provider):
    """
    Wander mode is an exploratory mode where an LLM is given a task and they begin to wander through space.
    As they wander, they drift in between conscious thought and popcorn-like subconscious thought
    The former is triggered by external stimuli andw when these stimuli come we will capture the recent high entropy
    infromation from the subconscious popcorn thoughts and then consider them with respect to the initial problem at hand.

    The conscious evaluator will attempt to connect them, thus functionalizing the verse-jumping algorithm
    outlined by Everything Everywhere All at Once.


    """
    return


def ots(
    command_parts,
    npc=None,
    model: str = NPCSH_VISION_MODEL,
    provider: str = NPCSH_VISION_PROVIDER,
    api_url: str = NPCSH_API_URL,
    api_key: str = None,
    stream: bool = False,
):
    # check if there is a filename
    if len(command_parts) > 1:
        filename = command_parts[1]
        file_path = os.path.join(os.getcwd(), filename)
        # Get user prompt about the image
        user_prompt = input(
            "Enter a prompt for the LLM about this image (or press Enter to skip): "
        )
        output = analyze_image(
            user_prompt, file_path, filename, npc=npc, model=model, provider=provider
        )
    else:
        output = capture_screenshot(npc=npc)
        user_prompt = input(
            "Enter a prompt for the LLM about this image (or press Enter to skip): "
        )
        output = analyze_image(
            user_prompt,
            output["file_path"],
            output["filename"],
            npc=npc,
            model=model,
            provider=provider,
            api_url=api_url,
            api_key=api_key,
            stream=stream,            
        )
    return {"messages": [], "output": output}  # Return the message


def get_help():
    output = """# Available Commands

/com [npc_file1.npc npc_file2.npc ...] # Alias for /compile.

/compile [npc_file1.npc npc_file2.npc ...] # Compiles specified NPC profile(s). If no arguments are provided, compiles all NPCs in the npc_profi

/exit or /quit # Exits the current NPC mode or the npcsh shell.

/help # Displays this help message.

/init # Initializes a new NPC project.

/notes # Enter notes mode.

/ots [filename] # Analyzes an image from a specified filename or captures a screenshot for analysis.

/rag <search_term> # Performs a RAG (Retrieval-Augmented Generation) search based on the search term provided.

/sample <question> # Asks the current NPC a question.

/set <model|provider|db_path> <value> # Sets the specified parameter. Enclose the value in quotes.

/sp [inherit_last=<n>] # Alias for /spool.

/spool [inherit_last=<n>] # Enters spool mode. Optionally inherits the last <n> messages.

/vixynt [filename=<filename>] <prompt> # Captures a screenshot and generates an image with the specified prompt.

/<subcommand> # Enters the specified NPC's mode.

/cmd <command/> # Execute a command using the current NPC's LLM.

/command <command/> # Alias for /cmd.

Tools within your npc_team directory can also be used as macro commands.


# Note
Bash commands and other programs can be executed directly. """
    return output


def execute_tool_command(
    tool: Tool,
    args: List[str],
    messages=None,
    npc: NPC = None,
) -> Dict[str, Any]:
    """
    Execute a tool command with the given arguments.
    """
    # Extract inputs for the current tool
    input_values = extract_tool_inputs(args, tool)

    # print(f"Input values: {input_values}")
    # Execute the tool with the extracted inputs

    tool_output = tool.execute(
        input_values,
        tool.tool_name,
        npc=npc,
    )

    return {"messages": messages, "output": tool_output}


def print_tools(tools):
    output = "Available tools:"
    for tool in tools:
        output += f"  {tool.tool_name}"
        output += f"   Description: {tool.description}"
        output += f"   Inputs: {tool.inputs}"
    return output


def execute_slash_command(
    command: str,
    npc: NPC = None,
    team: Team = None,
    messages=None,
    model: str = None,
    provider: str = None,
    api_url: str = None,
    conversation_id: str = None,
    stream: bool = False,
):
    """
    Function Description:
        Executes a slash command.
    Args:
        command : str : Command

    Keyword Args:
        embedding_model : None : Embedding model
        current_npc : None : Current NPC
        text_data : None : Text data
        text_data_embedded : None : Embedded text data
        messages : None : Messages
    Returns:
        dict : dict : Dictionary
    """

    command = command[1:]

    log_action("Command Executed", command)

    command_parts = command.split()
    command_name = command_parts[0] if len(command_parts) >= 1 else None
    args = command_parts[1:] if len(command_parts) >= 1 else []

    current_npc = npc
    if team is not None:
        if command_name in team.npcs:
            current_npc = team.npcs.get(command_name)
            output = f"Switched to NPC: {current_npc.name}"
        return {"messages": messages, "output": output, "current_npc": current_npc}
    print(command)
    print(command_name == "ots")
       
    if command_name == "compile" or command_name == "com":
        try:
            """ 

            if len(args) > 0:  # Specific NPC file(s) provided
                for npc_file in args:
                    # differentiate between .npc and .pipe
                    if npc_file.endswith(".pipe"):
                        # Initialize the PipelineRunner with the appropriate parameters
                        pipeline_runner = PipelineRunner(
                            pipeline_file=npc_file,  # Uses the current NPC file
                            db_path="~/npcsh_history.db",  # Ensure this path is correctly set
                            npc_root_dir="./npc_team",  # Adjust this to your actual NPC directory
                        )

                        # Execute the pipeline and capture the output
                        output = pipeline_runner.execute_pipeline()

                        # Format the output if needed
                        output = f"Compiled Pipeline: {output}\n"
                    elif npc_file.endswith(".npc"):
                        compiled_script = npc_compiler.compile(npc_file)

                        output = f"Compiled NPC profile: {compiled_script}\n"
            elif current_npc:  # Compile current NPC
                compiled_script = npc_compiler.compile(current_npc)
                output = f"Compiled NPC profile: {compiled_script}"
            else:  # Compile all NPCs in the directory
                output = ""
                for filename in os.listdir(npc_compiler.npc_directory):
                    if filename.endswith(".npc"):
                        try:
                            compiled_script = npc_compiler.compile(
                                npc_compiler.npc_directory + "/" + filename
                            )
                            output += (
                                f"Compiled NPC profile: {compiled_script['name']}\n"
                            )
                        except Exception as e:
                            output += f"Error compiling {filename}: {str(e)}\n"
             """
        except Exception as e:
            import traceback

            output = f"Error compiling NPC profile: {str(e)}\n{traceback.format_exc()}"
            print(output)
    elif command_name == "tools":
        return {"messages": messages, "output": print_tools('Team tools: '+
                                                            team.tools_dict.values() if team else []
                                                            +
                                                            'NPC Tools: '+
                                                            npc.tools_dict.values() if npc else []
                                                            )}
    elif command_name == "plan":
        return execute_plan_command(
            command,
            npc=npc,
            model=model,
            provider=provider,
            api_url=api_url,
            messages=messages,
        )
    elif command_name == "trigger":
        return execute_trigger_command(
            command,
            npc=npc,
            model=model,
            provider=provider,
            api_url=api_url,
            messages=messages,
        )

    elif command_name == "plonk":
        request = " ".join(args)
        plonk_call = plonk(
            request, action_space, model=model, provider=provider, npc=npc
        )
        return {"messages": messages, "output": plonk_call, "current_npc": current_npc}
    elif command_name == "wander":
        return enter_wander_mode(args, messages, npc_compiler, npc, model, provider)


        
        
    elif command_name == "flush":
        n = float("inf")  # Default to infinite
        for arg in args:
            if arg.startswith("n="):
                try:
                    n = int(arg.split("=")[1])
                except ValueError:
                    return {
                        "messages": messages,
                        "output": "Error: 'n' must be an integer." + "\n",
                    }

        flush_result = flush_messages(n, messages)
        return flush_result  # Return the result of flushing messages

    # Handle /rehash command
    elif command_name == "rehash":
        rehash_result = rehash_last_message(
            conversation_id, model=model, provider=provider, npc=npc
        )
        return rehash_result  # Return the result of rehashing last message

    elif command_name == "pipe":
        # need to fix
        if len(args) > 0:  # Specific NPC file(s) provided
            for npc_file in args:
                # differentiate between .npc and .pipe
                pipeline_runner = PipelineRunner(
                    pipeline_file=npc_file,  # Uses the current NPC file
                    db_path="~/npcsh_history.db",  # Ensure this path is correctly set
                    npc_root_dir="./npc_team",  # Adjust this to your actual NPC directory
                )

                # run through the steps in the pipe
    elif command_name == "select":
        query = " ".join([command_name] + args)  # Reconstruct full query

        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                rows = cursor.fetchall()

                if not rows:
                    output = "No results found"
                else:
                    # Get column names
                    columns = [description[0] for description in cursor.description]

                    # Format output as table
                    table_lines = []
                    table_lines.append(" | ".join(columns))
                    table_lines.append("-" * len(table_lines[0]))

                    for row in rows:
                        table_lines.append(" | ".join(str(col) for col in row))

                    output = "\n".join(table_lines)

                return {"messages": messages, "output": output}

        except sqlite3.Error as e:
            output = f"Database error: {str(e)}"
            return {"messages": messages, "output": output}
    elif command_name == "init":
        output = initialize_npc_project()
        return {"messages": messages, "output": output}
    elif (
        command.startswith("vixynt")
        or command.startswith("vix")
        or (command.startswith("v") and command[1] == " ")
    ):
        # check if "filename=..." is in the command
        filename = None
        if "filename=" in command:
            filename = command.split("filename=")[1].split()[0]
            command = command.replace(f"filename={filename}", "").strip()
        # Get user prompt about the image BY joining the rest of the arguments
        user_prompt = " ".join(command.split()[1:])

        output = generate_image(
            user_prompt, npc=npc, filename=filename, model=model, provider=provider
        )

    elif command_name == "ots":
        print('fasdh')
        return {"messages":messages, "output":ots(
            command_parts, model=model, provider=provider, npc=npc, api_url=api_url, 
            stream=stream
        )}
    elif command_name == "help":  # New help command
        print(get_help())
        return {
            "messages": messages,
            "output": get_help(),
        }

    elif command_name == "whisper":
        # try:
        messages = enter_whisper_mode(npc=npc)
        output = "Exited whisper mode."
        # except Exception as e:
        #    print(f"Error entering whisper mode: {str(e)}")
        #    output = "Error entering whisper mode"

    elif command_name == "notes":
        output = enter_notes_mode(npc=npc)
    elif command_name == "data":
        # print("data")
        output = enter_data_mode(npc=npc)
        # output = enter_observation_mode(, npc=npc)
    elif command_name == "cmd" or command_name == "command":
        output = execute_llm_command(
            command,
            npc=npc,
            stream=stream,
            messages=messages,
        )

    elif command_name == "search":
        result = execute_search_command(
            command,
            messages=messages,
        )
        messages = result["messages"]
        output = result["output"]
        return {
            "messages": messages,
            "output": output,
            "current_npc": current_npc,
        }
    elif command_name == "rag":
        result = execute_rag_command(command, messages=messages)
        messages = result["messages"]
        output = result["output"]
        return {
            "messages": messages,
            "output": output,
            "current_npc": current_npc,
        }

    elif command_name == "roll":

        output = generate_video(
            command,
            model=NPCSH_VIDEO_GEN_MODEL,
            provider=NPCSH_VIDEO_GEN_PROVIDER,
            npc=npc,
            messages=messages,
        )
        messages = output["messages"]
        output = output["output"]

    elif command_name == "set":
        parts = command.split()
        if len(parts) == 3 and parts[1] in ["model", "provider", "db_path"]:
            output = execute_set_command(parts[1], parts[2])
        else:
            return {
                "messages": messages,
                "output": "Invalid set command. Usage: /set [model|provider|db_path] 'value_in_quotes' ",
            }
    elif command_name == "search":
        output = execute_search_command(
            command,
            messages=messages,
        )
        messages = output["messages"]
        # print(output, type(output))
        output = output["output"]
        # print(output, type(output))
    elif command_name == "sample":
        output = execute_llm_question(
            " ".join(command.split()[1:]),  # Skip the command name
            npc=npc,
            messages=[],
            model=model,
            provider=provider,
            stream=stream,
        )
    elif command_name == "spool" or command_name == "sp":
        inherit_last = 0
        device = "cpu"
        rag_similarity_threshold = 0.3
        for part in args:
            if part.startswith("inherit_last="):
                try:
                    inherit_last = int(part.split("=")[1])
                except ValueError:
                    return {
                        "messages": messages,
                        "output": "Error: inherit_last must be an integer",
                    }
            if part.startswith("device="):
                device = part.split("=")[1]
            if part.startswith("rag_similarity_threshold="):
                rag_similarity_threshold = float(part.split("=")[1])
            if part.startswith("model="):
                model = part.split("=")[1]

            if part.startswith("provider="):
                provider = part.split("=")[1]
            if part.startswith("api_url="):
                api_url = part.split("=")[1]
            if part.startswith("api_key="):
                api_key = part.split("=")[1]

                # load the npc properly

        match = re.search(r"files=\s*\[(.*?)\]", command)
        files = []
        if match:
            # Extract file list from the command
            files = [
                file.strip().strip("'").strip('"') for file in match.group(1).split(",")
            ]

            # Call the enter_spool_mode with the list of files
        else:
            files = None

        if len(command_parts) >= 2 and command_parts[1] == "reattach":
            command_history = CommandHistory()
            last_conversation = command_history.get_last_conversation_by_path(
                os.getcwd()
            )
            print(last_conversation)
            if last_conversation:
                spool_context = [
                    {"role": part["role"], "content": part["content"]}
                    for part in last_conversation
                ]

                print(f"Reattached to previous conversation:\n\n")
                output = enter_spool_mode(
                    inherit_last,
                    files=files,
                    npc=npc,
                    model=model,
                    provider=provider,
                    rag_similarity_threshold=rag_similarity_threshold,
                    device=device,
                    messages=spool_context,
                    conversation_id=conversation_id,
                    stream=stream,
                )
                return {"messages": output["messages"], "output": output}

            else:
                return {"messages": [], "output": "No previous conversation found."}

        output = enter_spool_mode(
            inherit_last,
            files=files,
            npc=npc,
            rag_similarity_threshold=rag_similarity_threshold,
            device=device,
            conversation_id=conversation_id,
            stream=stream,
        )
        return {"messages": output["messages"], "output": output}

    elif npc is not None:
        if command_name in npc.tools_dict:
            tool = npc.tools_dict.get(command_name) or team.tools_dict.get(command_name)
            return execute_tool_command(
                tool,
                args,
                messages,
                npc=npc,
            )
    elif team is not None:
        if command_name in team.tools_dict:
            tool = team.tools_dict.get(command_name)
            return execute_tool_command(
                tool,
                args,
                messages,
                npc=npc,
            )
    output = f"Unknown command: {command_name}"

    return {
        "messages": messages,
        "output": output,
        "current_npc": current_npc,
    }


def execute_set_command(command: str, value: str) -> str:
    """
    Function Description:
        This function sets a configuration value in the .npcshrc file.
    Args:
        command: The command to execute.
        value: The value to set.
    Keyword Args:
        None
    Returns:
        A message indicating the success or failure of the operation.
    """

    config_path = os.path.expanduser("~/.npcshrc")

    # Map command to environment variable name
    var_map = {
        "model": "NPCSH_CHAT_MODEL",
        "provider": "NPCSH_CHAT_PROVIDER",
        "db_path": "NPCSH_DB_PATH",
    }

    if command not in var_map:
        return f"Unknown setting: {command}"

    env_var = var_map[command]

    # Read the current configuration
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            lines = f.readlines()
    else:
        lines = []

    # Check if the property exists and update it, or add it if it doesn't exist
    property_exists = False
    for i, line in enumerate(lines):
        if line.startswith(f"export {env_var}="):
            lines[i] = f"export {env_var}='{value}'\n"
            property_exists = True
            break

    if not property_exists:
        lines.append(f"export {env_var}='{value}'\n")

    # Save the updated configuration
    with open(config_path, "w") as f:
        f.writelines(lines)

    return f"{command.capitalize()} has been set to: {value}"


def flush_messages(n: int, messages: list) -> dict:
    if n <= 0:
        return {
            "messages": messages,
            "output": "Error: 'n' must be a positive integer.",
        }

    removed_count = min(n, len(messages))  # Calculate how many to remove
    del messages[-removed_count:]  # Remove the last n messages

    return {
        "messages": messages,
        "output": f"Flushed {removed_count} message(s). Context count is now {len(messages)} messages.",
    }


def rehash_last_message(
    conversation_id: str,
    model: str,
    provider: str,
    npc: Any = None,
    stream: bool = False,
) -> dict:
    # Fetch the last message or command related to this conversation ID
    command_history = CommandHistory()
    last_message = command_history.get_last_conversation(conversation_id)
    if last_message is None:
        convo_id = command_history.get_most_recent_conversation_id()[0]
        last_message = command_history.get_last_conversation(convo_id)

    user_command = last_message[3]  # Assuming content is in the 4th column
    return check_llm_command(
        user_command,
        model=model,
        provider=provider,
        npc=npc,
        messages=None,
        stream=stream,
    )


def get_npc_from_command(command: str) -> Optional[str]:
    """
    Function Description:
        This function extracts the NPC name from a command string.
    Args:
        command: The command string.

    Keyword Args:
        None
    Returns:
        The NPC name if found, or None
    """

    parts = command.split()
    npc = None
    for part in parts:
        if part.startswith("npc="):
            npc = part.split("=")[1]
            break
    return npc


def open_terminal_editor(command: str) -> None:
    """
    Function Description:
        This function opens a terminal-based text editor.
    Args:
        command: The command to open the editor.
    Keyword Args:
        None
    Returns:
        None
    """

    try:
        os.system(command)
    except Exception as e:
        print(f"Error opening terminal editor: {e}")


def parse_piped_command(current_command):
    """
    Parse a single command for additional arguments.
    """
    # Use shlex to handle complex argument parsing
    if "/" not in current_command:
        return current_command, []

    try:
        command_parts = shlex.split(current_command)
        # print(command_parts)
    except ValueError:
        # Fallback if quote parsing fails
        command_parts = current_command.split()
        # print(command_parts)
    # Base command is the first part
    base_command = command_parts[0]

    # Additional arguments are the rest
    additional_args = command_parts[1:] if len(command_parts) > 1 else []

    return base_command, additional_args


def replace_pipe_outputs(command: str, piped_outputs: list, cmd_idx: int) -> str:
    """
    Replace {0}, {1}, etc. placeholders with actual piped outputs.

    Args:
        command (str): Command with potential {n} placeholders
        piped_outputs (list): List of outputs from previous commands

    Returns:
        str: Command with placeholders replaced
    """
    placeholders = [f"{{{cmd_idx-1}}}", f"'{{{cmd_idx-1}}}'", f'"{{{cmd_idx-1}}}"']
    if str(cmd_idx - 1) in command:
        for placeholder in placeholders:
            command = command.replace(placeholder, str(output))
    elif cmd_idx > 0 and len(piped_outputs) > 0:
        # assume to pipe the previous commands output to the next command
        command = command + " " + str(piped_outputs[-1])
    return command


def execute_command( 
    command: str,
    npc: NPC = None,
    team: Team = None,
    model: str = None,
    provider: str = None,
    api_key: str = None,
    api_url: str = None,
    messages: list = None,
    conversation_id: str = None,
    stream: bool = False,
    embedding_model=None,
):
    """
    Function Description:
        Executes a command, with support for piping outputs between commands.
    Args:
        command : str : Command

        db_path : str : Database path

    Keyword Args:
        embedding_model :  Embedding model
        current_npc : NPC : Current NPC
        messages : list : Messages
    Returns:
        dict : dict : Dictionary
    """
    output = ""
    if len(command.strip()) == 0:
        return {"messages": messages, "output": output, "current_npc": npc}

    if messages is None:
        messages = []

    # Split commands by pipe, preserving the original parsing logic
    commands = command.split("|")
    # print(commands)
    available_models = get_available_models()

    # Track piped output between commands
    piped_outputs = []

    for idx, single_command in enumerate(commands):
        # Modify command if there's piped output from previous command

        if idx > 0:
            single_command, additional_args = parse_piped_command(single_command)
            if len(piped_outputs) > 0:
                single_command = replace_pipe_outputs(
                    single_command, piped_outputs, idx
                )
            if len(additional_args) > 0:
                single_command = f"{single_command} {' '.join(additional_args)}"

        messages.append({"role": "user", "content": single_command})
        # print(messages)

        if model is None:
            # note the only situation where id expect this to take precedent is when a frontend is specifying the model
            # to pass through at each time
            model_override, provider_override, command = get_model_and_provider(
                single_command, available_models[0]
            )
            if model_override is None:
                model_override = os.getenv("NPCSH_CHAT_MODEL")
            if provider_override is None:
                provider_override = os.getenv("NPCSH_CHAT_PROVIDER")
        else:
            model_override = model
            provider_override = provider
        if single_command.startswith("/"):
            result = execute_slash_command(
                single_command,
                npc=npc,
                messages=messages,
                model=model_override,
                provider=provider_override,
                stream=stream,
            )
            ## deal with stream here

            output = result.get("output", "")
            new_messages = result.get("messages", None)
            npc = result.get("current_npc", npc)
        else:
            # print(single_command)
            try:
                command_parts = shlex.split(single_command)
                # print(command_parts)
            except ValueError as e:
                if "No closing quotation" in str(e):
                    # Attempt to close unclosed quotes
                    if single_command.count('"') % 2 == 1:
                        single_command += '"'
                    elif single_command.count("'") % 2 == 1:
                        single_command += "'"
                    try:
                        command_parts = shlex.split(single_command)
                    except ValueError:
                        # fall back to regular split
                        command_parts = single_command.split()
            if command_parts[0] in interactive_commands:
                print(f"Starting interactive {command_parts[0]} session...")
                return_code = start_interactive_session(
                    interactive_commands[command_parts[0]]
                )
                return {
                    "messages": messages,
                    "output": f"Interactive {command_parts[0]} session ended with return code {return_code}",
                    "npc": npc,
                }
            elif command_parts[0] == "cd":
                change_dir_result = change_directory(command_parts, messages)
                messages = change_dir_result["messages"]
                output = change_dir_result["output"]
            elif command_parts[0] in BASH_COMMANDS:
                if command_parts[0] in TERMINAL_EDITORS:
                    return {
                        "messages": messages,
                        "output": open_terminal_editor(command),
                        "npc": npc,
                    }
                elif command_parts[0] in ["cat", "find", "who", "open", "which"]:
                    if not validate_bash_command(command_parts):
                        output = "Error: Invalid command syntax or arguments"
                        output = check_llm_command(
                            command,
                            npc=npc,
                            team=team,
                            messages=messages,
                            model=model_override,
                            provider=provider_override,
                            stream=stream,
                        )

                    else:
                        try:
                            result = subprocess.run(
                                command_parts, capture_output=True, text=True
                            )
                            output = result.stdout + result.stderr
                        except Exception as e:
                            output = f"Error executing command: {e}"

                elif command.startswith("open "):
                    try:
                        path_to_open = os.path.expanduser(
                            single_command.split(" ", 1)[1]
                        )
                        absolute_path = os.path.abspath(path_to_open)
                        expanded_command = [
                            "open",
                            absolute_path,
                        ]
                        subprocess.run(expanded_command, check=True)
                        output = f"Launched: {command}"
                    except subprocess.CalledProcessError as e:
                        output = colored(f"Error opening: {e}", "red")
                    except Exception as e:
                        output = colored(f"Error executing command: {str(e)}", "red")

                # Rest of BASH_COMMANDS handling remains the same
                else:
                    try:
                        result = subprocess.run(
                            command_parts, capture_output=True, text=True
                        )
                        output = result.stdout
                        if result.stderr:
                            output += colored(f"\nError: {result.stderr}", "red")

                        colored_output = ""
                        for line in output.split("\n"):
                            parts = line.split()
                            if parts:
                                filepath = parts[-1]
                                color, attrs = get_file_color(filepath)
                                colored_filepath = colored(filepath, color, attrs=attrs)
                                colored_line = " ".join(parts[:-1] + [colored_filepath])
                                colored_output += colored_line + "\n"
                            else:
                                colored_output += line
                        output = colored_output.rstrip()

                        if not output and result.returncode == 0:
                            output = colored(
                                f"Command '{single_command}' executed successfully (no output).",
                                "green",
                            )
                        print(output)
                    except Exception as e:
                        output = colored(f"Error executing command: {e}", "red")

            else:
                output = check_llm_command(
                    single_command,
                    npc=npc,
                    team=team,
                    messages=messages,
                    model=model_override,
                    provider=provider_override,
                    stream=stream,
                    api_key=api_key,
                    api_url=api_url,
                )

        if isinstance(output, dict):
            response = output.get("output", "")
            new_messages = output.get("messages", None)
            if new_messages is not None:
                messages = new_messages
            output = response
        if output:
            if npc is not None:
                print(f"{npc.name}> ", end="")
            
            if not stream:
                try:
                    render_markdown(output)
                except AttributeError:
                    print(output)

                piped_outputs.append(f'"{output}"')

                try:
                    # Prepare text to embed (both command and response)
                    texts_to_embed = [command, str(output) if output else ""]

                    # Generate embeddings
                    embeddings = get_embeddings(
                        texts_to_embed,
                    )

                    # Prepare metadata
                    metadata = [
                        {
                            "type": "command",
                            "timestamp": datetime.datetime.now().isoformat(),
                            "path": os.getcwd(),
                            "npc": npc.name if npc else None,
                            "conversation_id": conversation_id,
                        },
                        {
                            "type": "response",
                            "timestamp": datetime.datetime.now().isoformat(),
                            "path": os.getcwd(),
                            "npc": npc.name if npc else None,
                            "conversation_id": conversation_id,
                        },
                    ]
                    embedding_model = os.environ.get("NPCSH_EMBEDDING_MODEL")
                    embedding_provider = os.environ.get("NPCSH_EMBEDDING_PROVIDER")
                    collection_name = (
                        f"{embedding_provider}_{embedding_model}_embeddings"
                    )

                    try:
                        collection = chroma_client.get_collection(collection_name)
                    except Exception as e:
                        print(f"Warning: Failed to get collection: {str(e)}")
                        print("Creating new collection...")
                        collection = chroma_client.create_collection(collection_name)
                    date_str = datetime.datetime.now().isoformat()
                    current_ids = [f"cmd_{date_str}", f"resp_{date_str}"]

                    collection.add(
                        embeddings=embeddings,
                        documents=texts_to_embed,  
                        metadatas=metadata, 
                        ids=current_ids,
                    )

                except Exception as e:
                    print(f"Warning: Failed to store embeddings: {str(e)}")

    return {
        "messages": messages,
        "output": output,
        "conversation_id": conversation_id,
        "model": model,
        "current_path": os.getcwd(),
        "provider": provider,
        "npc": npc ,
        "team": team,
    }
def execute_command_stream(
    command: str,
    current_npc: NPC = None,
    team: Team = None,
    model: str = None,
    provider: str = None,
    messages: list = None,
):
    """
    Function Description:
        Executes a command, with support for piping outputs between commands.
    Args:
        command : str : Command

        db_path : str : Database path

    Keyword Args:
        embedding_model : Union[SentenceTransformer, Any] : Embedding model
        current_npc : NPC : Current NPC
        messages : list : Messages
    Returns:stream
        dict : dict : Dictionary
    """
    subcommands = []
    output = ""
    location = os.getcwd()
    db_conn = sqlite3.connect(db_path)

    # Split commands by pipe, preserving the original parsing logic
    commands = command.split("|")
    available_models = get_available_models()

    # Track piped output between commands
    piped_outputs = []

    for idx, single_command in enumerate(commands):
        # Modify command if there's piped output from previous command
        if idx > 0:
            single_command, additional_args = parse_piped_command(single_command)
            if len(piped_outputs) > 0:
                single_command = replace_pipe_outputs(
                    single_command, piped_outputs, idx
                )
            if len(additional_args) > 0:
                single_command = f"{single_command} {' '.join(additional_args)}"
        messages.append({"role": "user", "content": single_command})
        if model is None:
            # note the only situation where id expect this to take precedent is when a frontend is specifying the model
            # to pass through at each time
            model_override, provider_override, command = get_model_and_provider(
                single_command, available_models[0]
            )
            if model_override is None:
                model_override = os.getenv("NPCSH_CHAT_MODEL")
            if provider_override is None:
                provider_override = os.getenv("NPCSH_CHAT_PROVIDER")
        else:
            model_override = model
            provider_override = provider

        # Rest of the existing logic remains EXACTLY the same
        # print(model_override, provider_override)
        if current_npc is None:
            valid_npcs = get_db_npcs(db_path)

            npc_name = get_npc_from_command(command)
            if npc_name is None:
                npc_name = "sibiji"  # Default NPC
            npc_path = get_npc_path(npc_name, db_path)
            npc = NPC(file=npc_path, db_conn= db_conn)
        else:
            npc = current_npc
        # print(single_command.startswith("/"))
        if single_command.startswith("/"):
            return execute_slash_command(
                single_command,
                valid_npcs,
                npc=npc,
                messages=messages,
                model=model_override,
                provider=provider_override,
                db_conn= db_conn,
                stream=True,
            )
        else:  # LLM command processing with existing logic
            return check_llm_command(
                single_command,
                npc=npc,
                team=team,
                messages=messages,
                model=model_override,
                provider=provider_override,
                stream=True,
            )


def enter_whisper_mode(
    messages: list = None,
    npc: Any = None,
    team: Team = None,
    spool=False,
    continuous=False,
    stream=True,
    tts_model="kokoro",
    voice="af_heart",  # Default voice,
) -> Dict[str, Any]:
    # Initialize state
    running = True
    is_recording = False
    recording_data = []
    buffer_data = []
    last_speech_time = 0

    print("Entering whisper mode. Initializing...")

    # Update the system message to encourage concise responses
    concise_instruction = "Please provide brief responses of 1-2 sentences unless the user specifically asks for more detailed information. Keep responses clear and concise."

    model = select_model() if npc is None else npc.model or NPCSH_CHAT_MODEL
    provider = (
        NPCSH_CHAT_PROVIDER if npc is None else npc.provider or NPCSH_CHAT_PROVIDER
    )
    api_url = NPCSH_API_URL if npc is None else npc.api_url or NPCSH_API_URL

    print(f"\nUsing model: {model} with provider: {provider}")

    system_message = get_system_message(npc) if npc else "You are a helpful assistant."

    # Add conciseness instruction to the system message
    system_message = system_message + " " + concise_instruction

    if messages is None:
        messages = [{"role": "system", "content": system_message}]
    elif messages and messages[0]["role"] == "system":
        # Update the existing system message
        messages[0]["content"] = messages[0]["content"] + " " + concise_instruction
    else:
        messages.insert(0, {"role": "system", "content": system_message})

    kokoro_pipeline = None
    if tts_model == "kokoro":
        try:
            from kokoro import KPipeline
            import soundfile as sf

            kokoro_pipeline = KPipeline(lang_code="a")
            print("Kokoro TTS model initialized")
        except ImportError:
            print("Kokoro not installed, falling back to gTTS")
            tts_model = "gtts"

    # Initialize PyAudio
    pyaudio_instance = pyaudio.PyAudio()
    audio_stream = None  # We'll open and close as needed
    transcription_queue = queue.Queue()

    # Create and properly use the is_speaking event
    is_speaking = threading.Event()
    is_speaking.clear()  # Not speaking initially

    speech_queue = queue.Queue(maxsize=20)
    speech_thread_active = threading.Event()
    speech_thread_active.set()

    def speech_playback_thread():
        nonlocal running, audio_stream

        while running and speech_thread_active.is_set():
            try:
                # Get next speech item from queue
                if not speech_queue.empty():
                    text_to_speak = speech_queue.get(timeout=0.1)

                    # Only process if there's text to speak
                    if text_to_speak.strip():
                        # IMPORTANT: Set is_speaking flag BEFORE starting audio output
                        is_speaking.set()

                        # Safely close the audio input stream before speaking
                        current_audio_stream = audio_stream
                        audio_stream = (
                            None  # Set to None to prevent capture thread from using it
                        )

                        if current_audio_stream and current_audio_stream.is_active():
                            current_audio_stream.stop_stream()
                            current_audio_stream.close()

                        print(f"Speaking full response...")

                        # Generate and play speech
                        generate_and_play_speech(text_to_speak)

                        # Delay after speech to prevent echo
                        time.sleep(0.005 * len(text_to_speak))
                        print(len(text_to_speak))

                        # Clear the speaking flag to allow listening again
                        is_speaking.clear()
                else:
                    time.sleep(0.5)
            except Exception as e:
                print(f"Error in speech thread: {e}")
                is_speaking.clear()  # Make sure to clear the flag if there's an error
                time.sleep(0.1)

    def safely_close_audio_stream(stream):
        """Safely close an audio stream with error handling"""
        if stream:
            try:
                if stream.is_active():
                    stream.stop_stream()
                stream.close()
            except Exception as e:
                print(f"Error closing audio stream: {e}")

    # Start speech thread
    speech_thread = threading.Thread(target=speech_playback_thread)
    speech_thread.daemon = True
    speech_thread.start()

    def generate_and_play_speech(text):
        try:
            # Create a temporary file for audio
            unique_id = str(time.time()).replace(".", "")
            temp_dir = tempfile.gettempdir()
            wav_file = os.path.join(temp_dir, f"temp_{unique_id}.wav")

            # Generate speech based on selected TTS model
            if tts_model == "kokoro" and kokoro_pipeline:
                # Use Kokoro for generation
                generator = kokoro_pipeline(text, voice=voice)

                # Get the audio from the generator
                for _, _, audio in generator:
                    # Save audio to WAV file
                    import soundfile as sf

                    sf.write(wav_file, audio, 24000)
                    break  # Just use the first chunk for now
            else:
                # Fall back to gTTS
                mp3_file = os.path.join(temp_dir, f"temp_{unique_id}.mp3")
                tts = gTTS(text=text, lang="en", slow=False)
                tts.save(mp3_file)
                convert_mp3_to_wav(mp3_file, wav_file)

            # Play the audio
            wf = wave.open(wav_file, "rb")
            p = pyaudio.PyAudio()

            stream = p.open(
                format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
            )

            data = wf.readframes(4096)
            while data and running:
                stream.write(data)
                data = wf.readframes(4096)

            stream.stop_stream()
            stream.close()
            p.terminate()

            # Cleanup temp files
            try:
                if os.path.exists(wav_file):
                    os.remove(wav_file)
                if tts_model == "gtts" and "mp3_file" in locals():
                    if os.path.exists(mp3_file):
                        os.remove(mp3_file)
            except Exception as e:
                print(f"Error removing temp file: {e}")

        except Exception as e:
            print(f"Error in TTS process: {e}")

    # Modified speak_text function that just queues text
    def speak_text(text):
        speech_queue.put(text)

    def process_input(user_input):
        nonlocal messages

        # Add user message
        messages.append({"role": "user", "content": user_input})

        # Process with LLM and collect the ENTIRE response first
        try:
            full_response = ""

            # Use get_stream for streaming response
            check = check_llm_command(
                user_input,
                npc=npc,
                team=team,
                messages=messages,
                model=model,
                provider=provider,
                stream=True,
                whisper=True,
            )

            # Collect the entire response first
            for chunk in check:
                if chunk:
                    chunk_content = "".join(
                        choice.delta.content
                        for choice in chunk.choices
                        if choice.delta.content is not None
                    )

                    full_response += chunk_content

                    # Show progress in console
                    print(chunk_content, end="", flush=True)

            print("\n")  # End the progress display

            # Process and speak the entire response at once
            if full_response.strip():
                processed_text = process_text_for_tts(full_response)
                speak_text(processed_text)

            # Add assistant's response to messages
            messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            print(f"Error in LLM response: {e}")
            speak_text("I'm sorry, there was an error processing your request.")

    # Function to capture and process audio
    def capture_audio():
        nonlocal is_recording, recording_data, buffer_data, last_speech_time, running, is_speaking
        nonlocal audio_stream, transcription_queue

        # Don't try to record if we're speaking
        if is_speaking.is_set():
            return False

        try:
            # Only create a new audio stream if we don't have one
            if audio_stream is None and not is_speaking.is_set():
                audio_stream = pyaudio_instance.open(
                    format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                )

            # Initialize or reset the recording variables
            is_recording = False
            recording_data = []
            buffer_data = []

            print("\nListening for speech...")

            while (
                running
                and audio_stream
                and audio_stream.is_active()
                and not is_speaking.is_set()
            ):
                try:
                    data = audio_stream.read(CHUNK, exception_on_overflow=False)
                    if data:
                        audio_array = np.frombuffer(data, dtype=np.int16)
                        audio_float = audio_array.astype(np.float32) / 32768.0

                        tensor = torch.from_numpy(audio_float).to(device)
                        speech_prob = vad_model(tensor, RATE).item()
                        current_time = time.time()

                        if speech_prob > 0.5:  # VAD threshold
                            last_speech_time = current_time
                            if not is_recording:
                                is_recording = True
                                print("\nSpeech detected, listening...")
                                recording_data.extend(buffer_data)
                                buffer_data = []
                            recording_data.append(data)
                        else:
                            if is_recording:
                                if (
                                    current_time - last_speech_time > 1
                                ):  # silence duration
                                    is_recording = False
                                    print("Speech ended, transcribing...")

                                    # Stop stream before transcribing
                                    safely_close_audio_stream(audio_stream)
                                    audio_stream = None

                                    # Transcribe in this thread to avoid race conditions
                                    transcription = transcribe_recording(recording_data)
                                    if transcription:
                                        transcription_queue.put(transcription)
                                    recording_data = []
                                    return True  # Got speech
                            else:
                                buffer_data.append(data)
                                if len(buffer_data) > int(
                                    0.65 * RATE / CHUNK
                                ):  # buffer duration
                                    buffer_data.pop(0)

                    # Check frequently if we need to stop capturing
                    if is_speaking.is_set():
                        safely_close_audio_stream(audio_stream)
                        audio_stream = None
                        return False

                except Exception as e:
                    print(f"Error processing audio frame: {e}")
                    time.sleep(0.1)

        except Exception as e:
            print(f"Error in audio capture: {e}")

        # Close stream if we exit without finding speech
        safely_close_audio_stream(audio_stream)
        audio_stream = None

        return False

    def process_text_for_tts(text):
        # Remove special characters that might cause issues in TTS
        text = re.sub(r"[*<>{}()\[\]&%#@^_=+~]", "", text)
        text = text.strip()
        # Add spaces after periods that are followed by words (for better pronunciation)
        text = re.sub(r"(\w)\.(\w)\.", r"\1 \2 ", text)
        text = re.sub(r"([.!?])(\w)", r"\1 \2", text)
        return text

    # Now that functions are defined, play welcome messages
    speak_text("Entering whisper mode. Please wait.")

    try:

        while running:

            # First check for typed input (non-blocking)
            import select
            import sys

            # Don't spam the console with prompts when speaking
            if not is_speaking.is_set():
                print(
                    "\Speak or type your message (or 'exit' to quit): ",
                    end="",
                    flush=True,
                )

            rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
            if rlist:
                user_input = sys.stdin.readline().strip()
                if user_input.lower() in ("exit", "quit", "goodbye"):
                    print("\nExiting whisper mode.")
                    break
                if user_input:
                    print(f"\nYou (typed): {user_input}")
                    process_input(user_input)
                    continue  # Skip audio capture this cycle

            # Then try to capture some audio (if no typed input)
            if not is_speaking.is_set():  # Only capture if not currently speaking
                got_speech = capture_audio()

                # If we got speech, process it
                if got_speech:
                    try:
                        transcription = transcription_queue.get_nowait()
                        print(f"\nYou (spoke): {transcription}")
                        process_input(transcription)
                    except queue.Empty:
                        pass
            else:
                # If we're speaking, just wait a bit without spamming the console
                time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nInterrupted by user.")

    finally:
        # Set running to False to signal threads to exit
        running = False
        speech_thread_active.clear()

        # Clean up audio resources
        safely_close_audio_stream(audio_stream)

        if pyaudio_instance:
            pyaudio_instance.terminate()

        print("\nExiting whisper mode.")
        speak_text("Exiting whisper mode. Goodbye!")
        time.sleep(1)
        cleanup_temp_files()

    return {"messages": messages, "output": "Whisper mode session ended."}


def get_context_string(messages):
    context = []
    for message in messages[-5:]:  # Get last 5 messages for context
        role = message.get("role", "")
        content = message.get("content", "")
        context.append(f"{role.capitalize()}: {content}")
    return "\n".join(context)


def input_with_timeout(prompt, timeout=0.1):
    """Non-blocking input function with a timeout."""
    import select
    import sys

    print(prompt, end="", flush=True)
    rlist, _, _ = select.select([sys.stdin], [], [], timeout)
    if rlist:
        return sys.stdin.readline().strip()
    return None


def enter_notes_mode(npc: Any = None) -> None:
    """
    Function Description:

    Args:

    Keyword Args:
        npc : Any : The NPC object.
    Returns:
        None

    """

    npc_name = npc.name if npc else "sibiji"
    print(f"Entering notes mode (NPC: {npc_name}). Type '/nq' to exit.")

    while True:
        note = input("Enter your note (or '/nq' to quit): ").strip()

        if note.lower() == "/nq":
            break

        save_note(note, npc)

    print("Exiting notes mode.")


def save_note(note: str, db_conn, npc: Any = None) -> None:
    """
    Function Description:
        This function is used to save a note.
    Args:
        note : str : The note to save.

    Keyword Args:
        npc : Any : The NPC object.
    Returns:
        None
    """
    current_dir = os.getcwd()
    timestamp = datetime.datetime.now().isoformat()
    npc_name = npc.name if npc else "base"
    cursor = conn.cursor()

    # Create notes table if it doesn't exist
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        note TEXT,
        npc TEXT,
        directory TEXT
    )
    """
    )

    # Insert the note into the database
    cursor.execute(
        """
    INSERT INTO notes (timestamp, note, npc, directory)
    VALUES (?, ?, ?, ?)
    """,
        (timestamp, note, npc_name, current_dir),
    )

    conn.commit()

    print("Note saved to database.")
    # save the note with the current datestamp to the current working directory
    with open(f"{current_dir}/note_{timestamp}.txt", "w") as f:
        f.write(note)


def enter_data_analysis_mode(npc: Any = None) -> None:
    """
    Function Description:
        This function is used to enter the data analysis mode.
    Args:

    Keyword Args:
        npc : Any : The NPC object.
    Returns:
        None
    """

    npc_name = npc.name if npc else "data_analyst"
    print(f"Entering data analysis mode (NPC: {npc_name}). Type '/daq' to exit.")

    dataframes = {}  # Dict to store dataframes by name
    context = {"dataframes": dataframes}  # Context to store variables
    messages = []  # For conversation history if needed

    while True:
        user_input = input(f"{npc_name}> ").strip()

        if user_input.lower() == "/daq":
            break

        # Add user input to messages for context if interacting with LLM
        messages.append({"role": "user", "content": user_input})

        # Process commands
        if user_input.lower().startswith("load "):
            # Command format: load <file_path> as <df_name>
            try:
                parts = user_input.split()
                file_path = parts[1]
                if "as" in parts:
                    as_index = parts.index("as")
                    df_name = parts[as_index + 1]
                else:
                    df_name = "df"  # Default dataframe name
                # Load data into dataframe
                df = pd.read_csv(file_path)
                dataframes[df_name] = df
                print(f"Data loaded into dataframe '{df_name}'")
            except Exception as e:
                print(f"Error loading data: {e}")

        elif user_input.lower().startswith("sql "):
            # Command format: sql <SQL query>
            try:
                query = user_input[4:]  # Remove 'sql ' prefix
                df = pd.read_sql_query(query, npc.db_conn)
                print(df)
                # Optionally store result in a dataframe
                dataframes["sql_result"] = df
                print("Result stored in dataframe 'sql_result'")

            except Exception as e:
                print(f"Error executing SQL query: {e}")

        elif user_input.lower().startswith("plot "):
            # Command format: plot <pandas plotting code>
            try:
                code = user_input[5:]  # Remove 'plot ' prefix
                # Prepare execution environment
                exec_globals = {"pd": pd, "plt": plt, **dataframes}
                exec(code, exec_globals)
                plt.show()
            except Exception as e:
                print(f"Error generating plot: {e}")

        elif user_input.lower().startswith("exec "):
            # Command format: exec <Python code>
            try:
                code = user_input[5:]  # Remove 'exec ' prefix
                # Prepare execution environment
                exec_globals = {"pd": pd, "plt": plt, **dataframes}
                exec(code, exec_globals)
                # Update dataframes with any new or modified dataframes
                dataframes.update(
                    {
                        k: v
                        for k, v in exec_globals.items()
                        if isinstance(v, pd.DataFrame)
                    }
                )
            except Exception as e:
                print(f"Error executing code: {e}")

        elif user_input.lower().startswith("help"):
            # Provide help information
            print(
                """
Available commands:
- load <file_path> as <df_name>: Load CSV data into a dataframe.
- sql <SQL query>: Execute SQL query.
- plot <pandas plotting code>: Generate plots using matplotlib.
- exec <Python code>: Execute arbitrary Python code.
- help: Show this help message.
- /daq: Exit data analysis mode.
"""
            )

        else:
            # Unrecognized command
            print("Unrecognized command. Type 'help' for a list of available commands.")

    print("Exiting data analysis mode.")


def enter_data_mode(npc: Any = None) -> None:
    """
    Function Description:
        This function is used to enter the data mode.
    Args:

    Keyword Args:
        npc : Any : The NPC object.
    Returns:
        None
    """
    npc_name = npc.name if npc else "data_analyst"
    print(f"Entering data mode (NPC: {npc_name}). Type '/dq' to exit.")

    exec_env = {
        "pd": pd,
        "np": np,
        "plt": plt,
        "os": os,
        "npc": npc,
    }

    while True:
        try:
            user_input = input(f"{npc_name}> ").strip()
            if user_input.lower() == "/dq":
                break
            elif user_input == "":
                continue

            # First check if input exists in exec_env
            if user_input in exec_env:
                result = exec_env[user_input]
                if result is not None:
                    if isinstance(result, pd.DataFrame):
                        print(result.to_string())
                    else:
                        print(result)
                continue

            # Then check if it's a natural language query
            if not any(
                keyword in user_input
                for keyword in [
                    "=",
                    "+",
                    "-",
                    "*",
                    "/",
                    "(",
                    ")",
                    "[",
                    "]",
                    "{",
                    "}",
                    "import",
                ]
            ):
                if "df" in exec_env and isinstance(exec_env["df"], pd.DataFrame):
                    df_info = {
                        "shape": exec_env["df"].shape,
                        "columns": list(exec_env["df"].columns),
                        "dtypes": exec_env["df"].dtypes.to_dict(),
                        "head": exec_env["df"].head().to_dict(),
                        "summary": exec_env["df"].describe().to_dict(),
                    }

                    analysis_prompt = f"""Based on this DataFrame info: {df_info}
                    Generate Python analysis commands to answer: {user_input}
                    Return each command on a new line. Do not use markdown formatting or code blocks."""

                    analysis_response = npc.get_llm_response(analysis_prompt).get(
                        "response", ""
                    )
                    analysis_commands = [
                        cmd.strip()
                        for cmd in analysis_response.replace("```python", "")
                        .replace("```", "")
                        .split("\n")
                        if cmd.strip()
                    ]
                    results = []

                    print("\nAnalyzing data...")
                    for cmd in analysis_commands:
                        if cmd.strip():
                            try:
                                result = eval(cmd, exec_env)
                                if result is not None:
                                    render_markdown(f"\n{cmd} ")
                                    if isinstance(result, pd.DataFrame):
                                        render_markdown(result.to_string())
                                    else:
                                        render_markdown(result)
                                    results.append((cmd, result))
                            except SyntaxError:
                                try:
                                    exec(cmd, exec_env)
                                except Exception as e:
                                    print(f"Error in {cmd}: {str(e)}")
                            except Exception as e:
                                print(f"Error in {cmd}: {str(e)}")

                    if results:
                        interpretation_prompt = f"""Based on these analysis results:
                        {[(cmd, str(result)) for cmd, result in results]}

                        Provide a clear, concise interpretation of what we found in the data.
                        Focus on key insights and patterns. Do not use markdown formatting."""

                        print("\nInterpretation:")
                        interpretation = npc.get_llm_response(
                            interpretation_prompt
                        ).get("response", "")
                        interpretation = interpretation.replace("```", "").strip()
                        render_markdown(interpretation)
                    continue

            # If not in exec_env and not natural language, try as Python code
            try:
                result = eval(user_input, exec_env)
                if result is not None:
                    if isinstance(result, pd.DataFrame):
                        print(result.to_string())
                    else:
                        print(result)
            except SyntaxError:
                exec(user_input, exec_env)
            except Exception as e:
                print(f"Error: {str(e)}")

        except KeyboardInterrupt:
            print("\nKeyboardInterrupt detected. Exiting data mode.")
            break
        except Exception as e:
            print(f"Error: {str(e)}")

    return


def enter_spool_mode(
    inherit_last: int = 0,
    model: str = None,
    provider: str = None,
    npc: Any = None,
    files: List[str] = None,  # New files parameter
    rag_similarity_threshold: float = 0.3,
    device: str = "cpu",
    messages: List[Dict] = None,
    conversation_id: str = None,
    stream: bool = False,
) -> Dict:
    """
    Function Description:
        This function is used to enter the spool mode where files can be loaded into memory.
    Args:

        inherit_last : int : The number of last commands to inherit.
        npc : Any : The NPC object.
        files : List[str] : List of file paths to load into the context.
    Returns:
        Dict : The messages and output.

    """

    command_history = CommandHistory()
    npc_info = f" (NPC: {npc.name})" if npc else ""
    print(f"Entering spool mode{npc_info}. Type '/sq' to exit spool mode.")

    spool_context = (
        messages.copy() if messages else []
    )  # Initialize context with messages

    loaded_content = {}  # New dictionary to hold loaded content

    # Create conversation ID if not provided
    if not conversation_id:
        conversation_id = start_new_conversation()

    command_history = CommandHistory()
    # Load specified files if any
    if files:
        for file in files:
            extension = os.path.splitext(file)[1].lower()
            try:
                if extension == ".pdf":
                    content = load_pdf(file)["texts"].iloc[0]
                elif extension == ".csv":
                    content = load_csv(file)
                else:
                    print(f"Unsupported file type: {file}")
                    continue
                loaded_content[file] = content
                print(f"Loaded content from: {file}")
            except Exception as e:
                print(f"Error loading {file}: {str(e)}")

    # Add system message to context
    system_message = get_system_message(npc) if npc else "You are a helpful assistant."
    if len(spool_context) > 0:
        if spool_context[0]["role"] != "system":
            spool_context.insert(0, {"role": "system", "content": system_message})
    else:
        spool_context.append({"role": "system", "content": system_message})
    # Inherit last n messages if specified
    if inherit_last > 0:
        last_commands = command_history.get_all(limit=inherit_last)
        for cmd in reversed(last_commands):
            spool_context.append({"role": "user", "content": cmd[2]})
            spool_context.append({"role": "assistant", "content": cmd[4]})

    if npc is not None:
        if model is None:
            model = npc.model
        if provider is None:
            provider = npc.provider

    while True:
        try:
            user_input = input("spool> ").strip()
            if len(user_input) == 0:
                continue
            if user_input.lower() == "/sq":
                print("Exiting spool mode.")
                break
            if user_input.lower() == "/rehash":  # Check for whisper command
                # send the most recent message
                print("Rehashing last message...")
                output = rehash_last_message(
                    conversation_id,
                    model=model,
                    provider=provider,
                    npc=npc,
                    stream=stream,
                )
                print(output["output"])
                messages = output.get("messages", [])
                output = output.get("output", "")

            if user_input.lower() == "/whisper":  # Check for whisper command
                messages = enter_whisper_mode(spool_context, npc)
                # print(messages)  # Optionally print output from whisper mode
                continue  # Continue with spool mode after exiting whisper mode

            if user_input.startswith("/ots"):
                command_parts = user_input.split()
                file_path = None
                filename = None

                # Handle image loading/capturing
                if len(command_parts) > 1:
                    filename = command_parts[1]
                    file_path = os.path.join(os.getcwd(), filename)
                else:
                    output = capture_screenshot(npc=npc)
                    if output and "file_path" in output:
                        file_path = output["file_path"]
                        filename = output["filename"]

                if not file_path or not os.path.exists(file_path):
                    print(f"Error: Image file not found at {file_path}")
                    continue

                # Get user prompt about the image
                user_prompt = input(
                    "Enter a prompt for the LLM about this image (or press Enter to skip): "
                )

                # Read image file as binary data
                try:
                    with open(file_path, "rb") as img_file:
                        img_data = img_file.read()

                    # Create an attachment for the image
                    image_attachment = {
                        "name": filename,
                        "type": guess_mime_type(filename),
                        "data": img_data,
                        "size": len(img_data),
                    }

                    # Save user message with image attachment
                    message_id = save_conversation_message(
                        command_history,
                        conversation_id,
                        "user",
                        (
                            user_prompt
                            if user_prompt
                            else f"Please analyze this image: {filename}"
                        ),
                        wd=os.getcwd(),
                        model=model,
                        provider=provider,
                        npc=npc.name if npc else None,
                        attachments=[image_attachment],
                    )

                    # Now use analyze_image which will process the image
                    output = analyze_image(
                        command_history,
                        user_prompt,
                        file_path,
                        filename,
                        npc=npc,
                        stream=stream,
                        message_id=message_id,  # Pass the message ID for reference
                    )

                    # Save assistant's response
                    if output and isinstance(output, str):
                        save_conversation_message(
                            command_history,
                            conversation_id,
                            "assistant",
                            output,
                            wd=os.getcwd(),
                            model=model,
                            provider=provider,
                            npc=npc.name if npc else None,
                        )

                    # Update spool context with this exchange
                    spool_context.append(
                        {"role": "user", "content": user_prompt, "image": file_path}
                    )
                    spool_context.append({"role": "assistant", "content": output})

                    if isinstance(output, dict) and "filename" in output:
                        message = f"Screenshot captured: {output['filename']}\nFull path: {output['file_path']}\nLLM-ready data available."
                    else:
                        message = output

                    render_markdown(
                        output["response"]
                        if isinstance(output["response"], str)
                        else str(output["response"])
                    )
                    continue

                except Exception as e:
                    print(f"Error processing image: {str(e)}")
                    continue

            # Prepare kwargs for get_conversation
            kwargs_to_pass = {}
            if npc:
                kwargs_to_pass["npc"] = npc
                if npc.model:
                    kwargs_to_pass["model"] = npc.model

                if npc.provider:
                    kwargs_to_pass["provider"] = npc.provider

            # Incorporate the loaded content into the prompt for conversation
            if loaded_content:
                context_content = ""
                for filename, content in loaded_content.items():
                    # now do a rag search with the loaded_content
                    retrieved_docs = rag_search(
                        user_input,
                        content,
                        similarity_threshold=rag_similarity_threshold,
                        device=device,
                    )
                    if retrieved_docs:
                        context_content += (
                            f"\n\nLoaded content from: {filename}\n{content}\n\n"
                        )
                if len(context_content) > 0:
                    user_input += f"""
                    Here is the loaded content that may be relevant to your query:
                        {context_content}
                    Please reference it explicitly in your response and use it for answering.
                    """

            # Add user input to spool context
            spool_context.append({"role": "user", "content": user_input})

            # Save user message to conversation history
            message_id = save_conversation_message(
                command_history,
                conversation_id,
                "user",
                user_input,
                wd=os.getcwd(),
                model=model,
                provider=provider,
                npc=npc.name if npc else None,
            )

            if stream:
                conversation_result = ""
                output = get_stream(spool_context, **kwargs_to_pass)
                conversation_result = print_and_process_stream(output, model, provider)
                conversation_result = spool_context + [
                    {"role": "assistant", "content": conversation_result}
                ]
            else:
                conversation_result = get_conversation(spool_context, **kwargs_to_pass)

            # Handle potential errors in conversation_result
            if isinstance(conversation_result, str) and "Error" in conversation_result:
                print(conversation_result)  # Print the error message
                continue  # Skip to the next loop iteration
            elif (
                not isinstance(conversation_result, list)
                or len(conversation_result) == 0
            ):
                print("Error: Invalid response from get_conversation")
                continue

            spool_context = conversation_result  # update spool_context

            # Extract assistant's reply, handling potential KeyError
            try:
                # print(spool_context[-1])
                # print(provider)
                if provider == "gemini":
                    assistant_reply = spool_context[-1]["parts"][0]
                else:
                    assistant_reply = spool_context[-1]["content"]

            except (KeyError, IndexError) as e:
                print(f"Error extracting assistant's reply: {e}")
                print(spool_context[-1])
                print(
                    f"Conversation result: {conversation_result}"
                )  # Print for debugging
                continue

            # Save assistant's response to conversation history
            save_conversation_message(
                command_history,
                conversation_id,
                "assistant",
                assistant_reply,
                wd=os.getcwd(),
                model=model,
                provider=provider,
                npc=npc.name if npc else None,
            )

            # sometimes claude responds with unfinished markdown notation. so we need to check if there are two sets
            # of markdown notation and if not, we add it. so if # markdown notations is odd we add one more
            if assistant_reply.count("```") % 2 != 0:
                assistant_reply = assistant_reply + "```"

            if not stream:
                render_markdown(assistant_reply)

        except (KeyboardInterrupt, EOFError):
            print("\nExiting spool mode.")
            break

    return {
        "messages": spool_context,
        "output": "\n".join(
            [msg["content"] for msg in spool_context if msg["role"] == "assistant"]
        ),
    }


def guess_mime_type(filename):
    """Guess the MIME type of a file based on its extension."""
    extension = os.path.splitext(filename)[1].lower()
    mime_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".bmp": "image/bmp",
        ".webp": "image/webp",
        ".pdf": "application/pdf",
        ".txt": "text/plain",
        ".csv": "text/csv",
        ".json": "application/json",
        ".md": "text/markdown",
    }
    return mime_types.get(extension, "application/octet-stream")
